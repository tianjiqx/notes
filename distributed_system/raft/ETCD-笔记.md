## ETCD-笔记

## 1. 简介





## 2. 原理

### 2.1 Raft库

该库仅实现了 Raft 算法， 需要用户，自己实现网络和存储层：

- 网络传输层， node 间传递消息
- 存储层，持久化 Raft 日志和状态



官方模块使用示例参考：[raftexample](https://github.com/etcd-io/etcd/tree/main/contrib/raftexample)



当前已经被etcd、Kubernetes、Docker Swarm、Cloud Foundry Diego、CockroachDB、TiDB、Project Calico、Flannel、Hyperledger 等分布式系统所使用。



### 2.2 raftexample

组件构成

- http api server
  - 接受 http请求
- kvstore
  - 存储层，内存map实现的kv存储，实现了raftNode需要的一些接口如快照
  - `kvstore.go`
  - 关键方法
    - `Lookup` 根据key，读取value
    - 创建时启动的独立线程，`readCommits` 从`commitC`通道中获取已经提交raft log，应用到本地的存储引擎，持久化
      - 其中若从通道中获取到nil值，调用`loadSnapshot()`  根据快照更新整个kv。
      - 获取到正常的数据日志时，解析数据，写到map中，然后关闭commit中包含的`applyDoneC`通道
    - `Propose` 提议，即是将kv值，写到 `proposeC` 通道， 作为leader和leaseholder 写raft log。自身的应用raft log 依然通过`readCommits` 获取。
    - `getSnapshot` 根据用户数据map创建快照(map 转json的字节数组)
    - `recoverFromSnapshot` 根据用户数据bytes数组快照，恢复为map
    - `loadSnapshot`  装载raftNode的快照结构
- raftNode
  - 复制层，raft 对等节点的定义，完成raft log同步，集群节点变更同步等功能
  - `raft.go`
  - 关键成员
    - `proposeC` string类型通道，kvstore写入的内容，和kvstore持有的同一个通道
    - `confChangeC` raftpb.ConfChange类型通道，节点变更信息通道
    - `commitC` 每个raftNode自己记录的已经提交的log的通道
    - `errorC`  raft会话错误信息通道？
    - `confState` 全局集群状态（节点，角色等）
    - `snapshotIndex` 快照日志位置
    - `appliedIndex` 状态机已经应用位置
    - `transport *rafthttp.Transport` peers间网络通信服务
    -  raft 状态机
      - `node raft.Node`
      - `raftStorage *raft.MemoryStorage`
      - `wal *wal.WAL`
  - 关键方法
    - `startRaft` 启动RaftNode服务
      - `replayWAL` 回放wal日志
      - `serveRaft` 独立线程，select监听`httpstopc` 通道是否有stop消息
      - `serveChannels`  独立线程处理日志同步，同步状态机更新
    - `serveChannels`  
      - raft状态机raftStorage的快照中获取初始状态（confState，snapshotIndex，appliedIndex）
      - 启动独立线程循环select发送通道`proposeC`中的proposals，`confChangeC`中的节点状态信息
        - `Raft.Node.Propose()`  通过raft 状态机传递提议，写日志
        - `Raft.Node.roposeConfChange()` bytes数组形式的（kv）string 消息
        - 循环退出条件
          - `proposeC` 和 `confChangeC` 任意不存在，通道发生异常
        - 线程退出前，关闭`stopc`通道
      - 本线程，循环select接受通道的消息，更新自己raft节点状态
        - `ticker.C` 定时更新自己的逻辑时间戳，维护节点间心跳 
          - `Raft.Node.Tick()`
        - `node.Ready()` Ready通道，接收到准备好的日志条目
          - `Ready` 类型
            - Ready 封装了准备读取、保存到稳定存储、提交或发送给其他对等点的条目和消息。
            - Ready 中的所有字段都是只读的。
          - `wal.Save()` 写wal
          - `raftStorage.Append(rd.Entries)` 追加日志条目到raft内存存储引擎
          - `transport.Send()` 尝试发送到其他peers节点
            - 可能该日志就是从其他peers发过来的，就不发送了
          - `publishEntries()` 应用commited log，返回通道applyDoneC
          - `maybeTriggerSnapshot(applyDoneC)`  尝试写快照（默认间隔10000条日志），监听阻塞通道applyDoneC等待log 被应用，然后写快照
            - `raftStorage.Compact(compactIndex)`
              - 经过快照后，可以删除旧的wal log
          - `node.Advance()` 通知准备下一个Ready
        - `transport.ErrorC` 错误通道
        - `stopc` 接收到stop消息，关闭raftNode
      - defer 关闭wal，定时器ticker
    - `entriesToApply` 接收日志（committed log）数组，计算需要应用的已经提交的日志数组，扔掉小于appliedIndex的日志
    - `publishEntries` 写committed log 到 `commitC` 通道
      - 即如此使用`publishEntries(entriesToApply([]raftpb.Entry))`
      - 内部分数据日志，和节点增减日志类型
        - 数据日志，的data部分即为写入的（kv）string
      - 最终会返回一个`applyDoneC` 单大小的应用完成通道。



### 2.3 multi-raft

单raft以物理节点作为同步的单元。multi-raft，同步的单元是region，复制一段顺序范围的key的同步。

例如tidb 自增key的前5位，作为region键，散列key分片到不同的region，同时避免产生热点region写。

同步单元是region，但是并非为每个region创建一个raft 状态机，因为region数量远大于节点数量。并且region之间同心跳流量，也会随region数量线性增加

[CockroachDB](https://github.com/cockroachdb/cockroach) 在raft之上引入MultiRaft层，将整个节点范围的region作为一个组进行管理（缓存，批处理融合）。只需要节点相互间维持心跳即可。

tidb使用PD，做region的管理，负载均衡。

一个节点上的所有region，是可以共用一个raft状态机的。维持一个regin id与其他的map，如commitC，响应不同的region 已提交日志。



## 3. 使用



## REF

- [github: etcd](https://github.com/etcd-io/etcd)
- [官方文档-zh翻译](https://doczhcn.gitbook.io/etcd/index)
- [etcd raft doc](https://github.com/etcd-io/etcd/blob/main/raft/README.md)
- [一文入门ETCD](https://juejin.cn/post/6844904031186321416#heading-0)
- [etcd 快速入门](https://zhuanlan.zhihu.com/p/96428375)
- [etcd raft 设计与实现《一》](https://zhuanlan.zhihu.com/p/51063866)
- [etcd raft 设计与实现《二》](https://zhuanlan.zhihu.com/p/51065416) 
- [etcd-raft的线性一致读方法二：LeaseRead](https://zhuanlan.zhihu.com/p/31118381) 
- [etcd-raft的线性一致读方法一：ReadIndex](https://zhuanlan.zhihu.com/p/31050303) 
- [etcd-raft节点变更](https://zhuanlan.zhihu.com/p/29886900) 
- [etcd-raft snapshot实现分析](https://zhuanlan.zhihu.com/p/29865583)  

- [etcd-raft日志管理](https://zhuanlan.zhihu.com/p/29692778) 
- [etcd-raft网络传输组件实现分析](https://zhuanlan.zhihu.com/p/29207055) 

- [etcd-raft示例分析](https://zhuanlan.zhihu.com/p/29180575)
- [scaling-raft](https://www.cockroachlabs.com/blog/scaling-raft/)


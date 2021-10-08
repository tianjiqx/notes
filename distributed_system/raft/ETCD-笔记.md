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
  - 接受 http请求，包括用户写数据，手动节点变更
- kvstore
  - 存储层，内存map实现的kv存储，实现了raftNode需要的一些接口如快照
  - `kvstore.go`
  - 关键方法
    - `Lookup` 根据key，读取value
    - 创建时启动的独立线程，`readCommits()` 从`commitC`通道中获取已经提交raft log，应用到本地的存储引擎，持久化
      - 其中若从通道中获取到nil值，调用`loadSnapshot()`  根据快照更新整个kv。
        - 在raftNode写nil到commitC前，已经先保存快照到本地
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
        - `ercd/raft/node.go:StartNode()` 启动raft协议的node
        - node之间是对等，并且都可以发起提议通过`Propose()`
          - 看注释提到提议可能被丢失，需要用户重试
          - `raftexample_test.go:TestProposeOnCommit()` 方法测试3节点的集群，也是三个节点同时写提议
            - 如何保证每个节点日志index是正确的？
            - 没有leader？看其他博客提到非leader节点会转发msg，但是自己没看到。`etc/raft/node.go:stepWithWaitOption()` 直接写入`n.propc`通道，后续处理识别了吗？
              - `node.run()` 方法会接受通道中的数据
                - `stepLeader()` 似乎会将消息发送到leader
      - `raftStorage *raft.MemoryStorage`
        - 待被应用实现的存储层，MemoryStorage在内存中，维持部分最近的log entry，但是在WAL 会持久化日志，或者生成快照。
      - `wal *wal.WAL`
        - 持久化 log，读取快照等
  - 关键方法
    - `startRaft` 启动RaftNode服务
      - `replayWAL` 回放wal日志
      - `serveRaft` 独立线程，select监听`httpstopc` 通道是否有stop消息
        - 优雅停机
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
          - `wal.Save(rd.HardState, rd.Entries)` 写wal 日志，并且记录HardState 中任期，已经提交位置等信息
            - 如果是快照日志，先保存快照到本地，然后写nil到commitC，回放时装载快照，然后应用快照数据
              - 不直接应用快照，一方面避免多写，只接受commitC的日志，进行写存储，另一方面，不知道commitC是否为空，此时应用快照数据，可能导致被commitC中的旧log覆盖，导致数据错误。
          - `raftStorage.Append(rd.Entries)` leader追加日志条目到raft内存存储引擎（可能存在未提交日志）
            - followwer 通过`raft.handleAppendEntries()` 方法处理leader的日志。
          - `transport.Send()` 尝试发送到其他peers节点
            - leader的日志，会发送到其他peers
            - （理论上，如果我们先异步的发送日志到其他peers，然后再持久化日志，应该也不会出错，因为只有持久化之后，才会检查日志写再次更新commitIndex，即使发送去的另2个节点的新日志都因为一下崩溃，而未能保存，也不影响之前已经commit的日志）
              - 这样的方式，忽略网络开销，理论时间是写单节点日志的2倍时间（max（replic2,replic3）+ replic1）
          - `publishEntries(rc.entriesToApply(rd.CommittedEntries))` 应用commited log，返回通道applyDoneC
            - rd中的`CommittedEntries` 队列记录了待应用的已经提交的日志
          - `maybeTriggerSnapshot(applyDoneC)`  尝试写快照（默认间隔10000条日志），监听阻塞通道applyDoneC等待log 被应用，然后写快照
            - `raftStorage.Compact(compactIndex)`
              - 经过快照后，可以删除旧的wal log
              - follower的快照是如何触发的？
                - Leader、Follower独立的创建快照, 还是ready触发
          - `node.Advance()` 通知准备下一个Ready
        - `transport.ErrorC` 错误通道
        - `stopc` 接收到stop消息，关闭raftNode
      - defer 关闭wal，定时器ticker
    - `entriesToApply` 接收日志（committed log）数组，计算需要应用的已经提交的日志数组，扔掉小于appliedIndex的日志
    - `publishEntries` 写committed log 到 `commitC` 通道
      - 即如此使用`publishEntries(entriesToApply([]raftpb.Entry))`
      - 内部分数据日志，和节点增减日志类型
        - 数据日志的data部分即为写入的（kv）string
        - 节点状态日志，修改raftNode的confState，修改transport peers
      - 最终会返回一个`applyDoneC` 单大小的应用完成通道。



### 2.3 multi-raft

单raft以物理节点作为同步的单元。multi-raft，同步的单元是region，复制一段顺序范围的key的同步。

region:

- 预先切分，之后分裂
- 空间大小达到阈值进行分裂

例如tidb 自增key的前5位，作为region键，散列key分片到不同的region，同时避免产生热点region写。

同步单元是region，但是并非为每个region创建一个raft 状态机，因为region数量远大于节点数量。并且region之间同心跳流量，也会随region数量线性增加

[CockroachDB](https://github.com/cockroachdb/cockroach) 在raft之上引入MultiRaft层，将整个节点范围的region作为一个组进行管理（缓存，批处理融合）。只需要节点相互间维持心跳即可。

tidb使用PD，做region的管理，负载均衡。

一个节点上的所有region，是可以共用一个raft状态机的。维持一个regin id与其他的map，如commitC，响应不同的region 已提交日志。



问题：但是raft node如何管理其peer呢，非为region固定物理机器组成raft group。

4节点，region1 在 0,1,2 region2 在0,2,3 如何做到？

是为每个region启动一个raft 状态机（raft.Node）？但是共用raft.MemoryStorage和rafthttp.Transport？

当分配到一个新的region或者分裂region时，创建一个raft.Node？

因为，共用raft.MemoryStorage ，日志的各种index，也需要共用。



- tikv  raft log和用户数据 用2个 rockdb实例分别存储。 根据raftexample， 使用了raft 自带的 `raftStorage *raft.MemoryStorage`  差异区别？
  - MemoryStorage 实际在内存中，无法解决宕机问题，即开篇raft要求实现的存储层
  - tikv，会真正把日志落盘
    - `raft_log_engine/src/engine.rs` 日志存储层  `RaftLogEngine`
    - `raftstore/src/store/transport.rs` 网络层
  - 另外cockroach 实现的raft.Storage 接口 `replicaRaftStorage`
    - `pkg/kv/kvserver/replica.go`
    - `pkg/kv/kvserver/replica_raftstorage.go`



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
- [tikv overview](https://docs.pingcap.com/zh/tidb/stable/tikv-overview)
- [Elasticell-Multi-Raft实现](https://zhuanlan.zhihu.com/p/33047950)
- [TiKV 源码解析系列 - multi-raft 设计与实现](https://pingcap.com/zh/blog/the-design-and-implementation-of-multi-raft)
- [CockroachDB 源码闲逛 - I (meta ranges)](https://zhuanlan.zhihu.com/p/75452389)
- 《etcd技术内幕》- 百里燊  推荐


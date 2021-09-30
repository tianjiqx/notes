## ETCD-笔记

## 1. 简介





## 2. 原理

## 2.1 Raft库

该库仅实现了 Raft 算法， 需要用户，自己实现网络和存储层：

- 网络传输层， node 间传递消息
- 存储层，持久化 Raft 日志和状态



官方模块使用示例参考：

- https://github.com/etcd-io/etcd/tree/main/contrib/raftexample
- raftexample



当前已经被etcd、Kubernetes、Docker Swarm、Cloud Foundry Diego、CockroachDB、TiDB、Project Calico、Flannel、Hyperledger 等分布式系统所使用。



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


# PolarDB-笔记

## 1. 一致性与时间戳

**线性一致性Linearizabile**

> 如果我们能为每个操作分配一个时间**点**（称为 Linearization Point），该时间点位于操作执行的时间**段**之内，在时间**点**上得到的执行结果和这些操作事实上的执行结果一致，那么该系统是强一致，满足线性一致性。

**时间戳**

- 为系统中的事件建立一个先后关系
- 时间戳越大表示事件的顺序越靠后

**Lamport Clock**

- 最简单的时间戳实现方式，逻辑时间，记录事件的先后/因果关系（causality）
  - 思想：如果 A 事件导致了 B 事件，那么 A 的时间戳一定小于 B
  - 根据接收到的消息，更新 `Tlocal = max( Tmsg, Tlocal)  + 1`
- 自增整数表示时间

**HLC**（Hybrid Logical Clock）

- Lamport Clock的改进
- 高位存放物理时间戳（ms）、低位存放逻辑时间戳，当物理时间戳增加时逻辑位清零
  - 48bit 物理+16bit 逻辑

HLC/LC 不满足线性一致性

- 情形：事务A，B分别在不同的节点上独立执行（即无因果关系的情况下），那么此时A，B无法确定一个先后关系。
  - 事务A提交时间戳，小于B的读取时间戳，导致B无法读取A的写入，即使A已经提交。

CockroachDB的半同步时钟（semi-synchronized clocks）的改进，可以保证单行事务保证可线性化，多行事务依然无法保证。

- Read Restart 机制只能防止数据存在的情况，不能防止不存在的数据

**TSO** （Timestamp Oracle）

集中分配（TiDB 也使用该方法），全局单点为事务分配时间戳，真实时间。

时间戳格式

- 物理时钟 42bit （ms） + 逻辑时钟 16 bit + 保留位6 bit
- 租约机制，预可分配时间戳范围，保证换主不会导致分配时间重叠，导致的双主
- Grouping，批量的分配需要申请的时间戳。

缺点： 光速限制

全球，光速的延迟142ms，加上转发和路由，全球部署的各节点向TSO申请时间戳的实际延迟过大。

PolarDB 改进：

跨地域的CDC，使用基于HLC逻辑时钟。

**TrueTime: 原子钟与GPS**

去中心化的原子钟和GPS，本地来获取时间戳。

通过等待不确定窗口时间过去，来保证再次读请求所获取的时间戳更大，来保证快照读。

`TT.now() - Tstart > 2c , c=7ms`

PS:

关于时间戳，也是实现MVCC的一种方式，以及数据流系统也是基于时间戳处理数据。

通过给数据添加时间属性，可以视作是数据属性的解耦，区分冷热数据（或者增量数据/基线数据）。

数据带有版本，便可以使冷数据存储在更廉价的对象存储系统（S3，OSS）中，本地节点缓存一些新鲜的数据。

云原生的数据处理系统，也可以根据时间属性，进行存储。新鲜的数据，计算节点的内存中多副本维持，冷数据带有版本信息的缓存在本地SSD，持久化存储在S3,OSS中。查询时，根据时间戳查询，并如OB，ADB对增量和基线数据做融合，保证是快照读。

基于时间戳的版本，便无需要担心计算节点缓存的是否失效，只需要LRU淘汰过旧版本的数据。为免大规模淘汰，也可以配置策略，点查询，微块的查询缓存，大规模扫描直接访问S3等系统。

## REF

- POLARDB Meets Computational Storage:Efficiently Support Analytical Workloads in Cloud-Native Relational Database
- PolarFS: An Ultra-low Latency and Failure ResilientDistributed File System for Shared Storage Cloud Database
- Cloud-Native Database Systems at Alibaba: Opportunitiesand Challenges
- SIGMOD 2021 ：PolarDB Serverless: A Cloud Native Database for Disaggregated Data Centers
- Towards Cost-Effective and Elastic Cloud Database Deployment via Memory Disaggregation， VLDB 2021
- [什么是PolarDB](https://help.aliyun.com/document_detail/58764.html)
- [PolarDB开源社区](https://developer.aliyun.com/group/polardbforpg)
- [分布式数据库中的一致性与时间戳](https://zhuanlan.zhihu.com/p/360690247) 推荐
- [PolarDB-X 全局时间戳服务的设计](https://zhuanlan.zhihu.com/p/360160666)
- [知乎:PolarDB-X](https://www.zhihu.com/org/polardb-x)
- [云原生演进趋势下传统数据库升级实践](https://zhuanlan.zhihu.com/p/398581530)
  - PolarDB-X为PolarDB分布式版本，融合分布式SQL引擎与分布式自研存储X-DB，专注解决海量数据存储、超高并发吞吐、复杂计算与分析等问题。
- [深度干货｜云原生分布式数据库 PolarDB-X 的技术演进](https://zhuanlan.zhihu.com/p/420195295)
- [数据库内核那些事｜分布式数据库，挂掉两台机器会发生什么？](https://zhuanlan.zhihu.com/p/627920111)
  - 与其高概率少量不可用，不如不可用时（一个组挂两台）全体（分组内的分片）不可用，令分片数与可用性无关

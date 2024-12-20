
# 分布式存储系统

## 数据分片

### 一致性hash

一致性哈希（Consistent Hashing）是一种特殊的哈希算法，它在分布式系统中用于数据的分布和负载均衡，同时在节点加入或离开系统时，能够最小化重新分配数据的需求。

- 均匀分布：consistentHash方法确保所有的输入数据在哈希环上均匀分布。这意味着，即使在系统规模变化（例如，节点的增加或减少）时，数据也会尽可能均匀地重新分配到各个节点上。

- 最小化重新映射：当系统中的节点数量发生变化时，一致性哈希算法通过保持大部分数据在原有位置不变，从而最小化了数据重新映射的需求。这是因为一致性哈希算法在哈希环上为每个节点分配一个区间，而不是一个固定的位置。当一个节点离开或加入时，只需要重新分配该节点区间内的数据。

- 应用场景：consistentHash方法在分布式缓存、负载均衡、分布式存储等场景中非常有用。例如，在分布式缓存系统中，可以使用consistentHash方法来决定一个特定的缓存对象应该存储在哪个节点上。

goole guava 库实现 [guava consistentHash](https://guava.dev/releases/21.0/api/docs/com/google/common/hash/Hashing.html#consistentHash-com.google.common.hash.HashCode-int-)

注意：使用一致性hash 计算的分桶位置，再节点发生变化之后，需要自己处理对应的处理逻辑，比如重新调整桶数，关闭原来的工作处理任务，重新启动新的worker.


### ceph CRUSH 算法

Ceph是一个开源的分布式存储系统，CRUSH算法是其核心组件之一，用于处理数据的分布和副本放置策略。Controlled Scalable Decentralized Placement of Replicated Data，可控的、可扩展的、分布式的副本数据放置算法。

- 目标：CRUSH算法的主要目标是实现数据的均匀分布，确保集群中的每个节点都有相对均衡的数据负载。同时，它还要保证在节点故障时，数据的恢复和重新分布是高效的。

- 一致性哈希：CRUSH算法基于一致性哈希的原理，但它对其进行了扩展和改进。在CRUSH中，数据和节点都映射到一个哈希环上。通过这种方式，CRUSH能够处理节点的加入和退出，同时最小化数据迁移。

- 桶（Buckets）：CRUSH算法将数据分成多个桶，每个桶包含一定量的数据。这些桶在哈希环上均匀分布，并且每个桶都被分配到一个或多个节点上。当需要存储数据时，CRUSH会根据算法计算出应该将数据存储在哪些桶中。

- 副本策略：CRUSH算法支持灵活的副本策略。用户可以根据需要配置数据的副本数量以及副本之间的距离。例如，可以要求数据的两个副本位于不同的机架上，以提高数据的可靠性和容错能力。

- 动态调整：随着集群的扩展或缩减，CRUSH算法能够动态调整数据分布。当新节点加入集群时，CRUSH算法会计算出需要迁移的数据量，并将其转移到新节点上。同样，当节点离开集群时，CRUSH也会重新分配数据。

- 容错性：CRUSH算法考虑了节点故障的情况。通过合理的副本策略，即使部分节点发生故障，数据也能够被成功访问。此外，CRUSH算法还能够在节点恢复后，有效地将数据重新分布回集群中。

## REF

- [分布式存储（一）：分布式存储基础](https://zhuanlan.zhihu.com/p/686693198)
- [分布式存储（二）：GFS与Ceph](https://zhuanlan.zhihu.com/p/690991550)

- [Ceph CRUSH算法](https://cloud.tencent.com/developer/article/1664645)

- [Consistent Hashing and Random Trees (1997)](https://zhenghe.gitbook.io/open-courses/papers-we-love/consistent-hashing-and-random-trees-1997)

- [从一致性 hash 到 ceph crush](https://zhuanlan.zhihu.com/p/60963885)
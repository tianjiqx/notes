# Spark笔记

[TOC]

## 1. Spark简介

### 1.1 spark技术背景

**集群编程模型**，处理大规模数据，如MapReduce，Dryad。将分布式编程简化为自动提供位置感知的**调度**、**容错**以及**负载均衡**。

非循环的数据流模型：从稳定的物理存储（分布式文件系统）加载数据，传入一组确定性操作构成的DAG（有向无环图），然后写回稳定存储(保证容错)。DAG数据流图能够在运行时，自动实现任务的调度和故障恢复。

无法满足的场景：

- 机器学习和图应用中常用的迭代算法（每一步对数据执行相似的函数）
- 交互式的数据挖掘工具（用户反复查询一个数据子集）。基于数据流框架不明确支持工作集。需要将数据输出到磁盘，每次查询是重新加载。

RDD：弹性分布式数据集。支持基于工作集的应用，同时具有数据流模型特点：自动容错、位置感知调度和可伸缩性。

允许用户执行多个查询时，显示将工作集缓存在内存中（即RDD），供后续查询重用（RDD可以被多个子RDD处理），极大提升了查询速度。

RDD提供高度受限的共享内存模型，RDD是只读记录分区的集合。只能通过其他RDD只需确定的转换操作（map，join，groupBy）而创建。与分布式共享内存系统需要昂贵的检查点和回滚机制不同，RDD通过lineage重建丢失的分区：一个RDD包含了如何重其他RDD衍生所必须的相关信息。

RDD在性能上获取优势，**在于利用RDD之间的继承关系（宽窄依赖），保证容错性，对于窄依赖的关系，RDD之间无需持久化，直接内存重算。宽依赖视情况，持久化。**

### 1.2 优势

- 速度。基于内存运算，减少落盘次数。
- 易用。广泛的编程语言API接口，丰富的高级算法，便于快速构建不同的应用。支持shell模式，快速验证。
- 通用性。统一的解决方案，批处理，交互式查询（Spark SQL），实时流处理（Spark streaming）、机器学习，图计算，并且不损失性能。
- 可融合性。开源生态。可以使用YARN，Mesos作为资源管理和调度器，并处理所有Hadoop支持的数据，HDFS，Hbase，Cassandra等。也可以使用内置资源管理器和调度框架Standalone。





## 2.基本执行原理



### 2.1 Adaptive Query Execution (AQE) 自适应查询执行

Spark 3.0 Adaptive Query Execution (AQE) 是指在查询执行期间发生的查询重新优化。

基于运行时统计的动态规划和重新规划查询的框架，支持多种优化：

- 动态切换连接策略
- 动态合并 Shuffle 分区
- 动态处理倾斜连接



#### 2.1.1 动态切换连接策略

Spark 支持多种连接策略，其中广播哈希连接（broadcast hash join）通常是性能最高的，如果连接的一侧可以很好地适应内存（广播小表）。

Spark在生成计划时，依赖统计信息、推导，可能导致估计错误。导致计划决策的连接算法错过或者误用。

AQE，能够根据最准确的连接关系大小，在运行时重新规划，还未执行的连接策略。



#### 2.1.2 动态合并 Shuffle 分区

shuffle是一个昂贵的操作，影响shuffle效果的一个关键属性是分区的数量，最佳分区数取决于数据，但数据大小可能因阶段、查询到查询而有很大差异：

- 如果分区太少，那么每个分区的数据量可能非常大，处理这些大分区的任务可能需要将数据溢出到磁盘（例如，当涉及排序或聚合时），因此，减慢查询速度。
- 如果分区太多，那么每个分区的数据量可能会很小，并且会有很多小的网络数据来读取shuffle块，这也会因为I/O效率低下而导致查询速度变慢。拥有大量任务也会给 Spark 任务调度器带来更多负担。

为了解决这个问题，可以在开始时设置比较多的shuffle partition，然后在运行时通过查看shuffle文件的统计信息，将相邻的小分区合并成更大的分区。

![](spark笔记图片/blog-adaptive-query-execution-2.png)

例子：

`SELECT max(i) FROM tbl GROUP BY j;`

输入数据 tbl 相当小，因此在分组之前只有两个分区。

初始shuffle分区数设置为5，所以本地分组后，将部分分组的数据shuffle成5个分区。spark启动5个任务进行最终的聚合。



![](spark笔记图片/blog-adaptive-query-execution-3.png)

AQE 将中间三个小分区合并为一个，task数量。



#### 2.1.3 动态处理倾斜连接

数据倾斜在大规模数据上的连接是一种非常常见的现象。严重的倾斜，导致长尾任务的产生，降低查询性能。

AQE 倾斜连接优化会从随机文件统计信息中自动检测此类倾斜。

然后它将倾斜的分区拆分为更小的子分区，这些子分区将从另一侧分别连接到相应的分区。

![](spark笔记图片/blog-adaptive-query-execution-5.png)

上面的例子，表A的A0分区明显大于其他分区，AQE会将A0拆分成2个子分区，并将他们与B0都进行连接。

![](spark笔记图片/blog-adaptive-query-execution-6.png)











## REF

- [Spark底层执行原理详细解析](https://mp.weixin.qq.com/s/qotI36Kx3nOINKHdOEf6nQ)
- High performance spark 
- [如何在 Kyuubi 中使用 Spark 自适应查询执行 (AQE)](https://kyuubi.readthedocs.io/en/latest/deployment/spark/aqe.html)
- [自适应查询执行：在运行时加速 Spark SQL](https://databricks.com/blog/2020/05/29/adaptive-query-execution-speeding-up-spark-sql-at-runtime.html)


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



### 2.2 SparkSQL

![](spark笔记图片/Snipaste_2021-08-07_22-40-45.png)

- 前端
  - Analysis  
  - Logical Optimization  
- 后端
  - Physical Planning
    - 转换逻辑算子为物理算子
    - 挑选候选的物理执行计划（比如连接算法broadcast-hash-join, sort-merge-join）
    - 单个算子，产生多个具体的物理算子
      - partial agg -> shuffle -> final agg
  - Code Generation
    - WSCG model代替Volcano iterator model （Pull model; Driven by the final operator）
      - Push model; Driven by the head/source operator
      - ![](spark笔记图片/Snipaste_2021-08-07_23-04-03.png)
    - 将原来的一串操作（next连接），融合成执行生成的代码的单个WSCG操作
      - 实现
        - WSCG节点（WholeStageCodegen）包含的操作都是窄依赖
    - 优点：
      - 减少虚函数调用
      - 数据在CPU寄存器
      - SIMD
  - Execution
    - 物理计划的调度
      - 标量子查询Scalar subquery 切分成为单独的job
      - shuffle操作作为stage划分边界
      - 对本地分区的操作，在同一个stage中
      - ![](spark笔记图片/Snipaste_2021-08-07_23-17-44.png)
    - 执行
      - Stage
        - 一个Stage产生一个TaskSet，每个分区，对应一个该TaskSet的task
        - Task被发送到Executor上执行



### 2.3 高效的表达式计算

对于`a+b`这样的表达式计算，解释执行，通常需要如下7步。

![](spark笔记图片/Snipaste_2021-08-07_22-01-13.png)

解释执行的缺点：

- 虚函数调用
- 存在基于表达式类型的分支（分支预测失败问题）
- 创建对象，封装原生类型，额外的内存开销

利用运行时反射，进行代码生成，方式执行`a+b`:

![](spark笔记图片/Snipaste_2021-08-07_22-08-43.png)

```scala
val	left:	Int =	inputRow.getInt(0)	
val	right:	Int	=	inputRow.getInt(1)	
val	result:	Int	=	left	+	right	
resultRow.setInt(0,	result)	
```

代码生成方式执行优势：

- 更少的函数调用
- 不需要对原生类型进包装计算

![](spark笔记图片/Snipaste_2021-08-07_22-10-59.png)



### 2.4 spark 内存管理

- RDD storage（RDD cache()操作）
  - LRU
- Execution memory（shuffle ,agg buffer）
- 用户代码申请的内存空间

内存使用改进:

- Dynamic occupancy，共享，运行时借用其他区域的空闲内存
  - `spark.memory.storageFraction  `
- Off-Heap Memory  JVM堆外内存
  - spark.memory.offHeap.enabled  
  - spark.memory.offHeap.size  



### 2.5 向量化读

支持读取列存格式的数据

- parquet
- orc
- arrow
  - PySpark

DataSource v2 API提供对其他数据源的相互化读取。



## 3.开放生态

源码版本2021.07.22：

3a1db2ddd439a6df2a1dd896aab8420a9b45286b

### 3.1 DataSource 

Spark SQL 支持通过 DataFrame 接口对多种数据源进行操作。将DataFrame注册为临时视图，允许对其数据运行SQL查询。

`DataSource`是Spark SQL 中的**Pluggable Data Provider Framework**的重要组成部分。

**关键接口**（`sql/core/src/main/scala/org/apache/spark/sql/sources/interfaces.scala`）:

- `CreatableRelationProvider` 保存接口（trait）
  - 根据保存模式，保存结构化查询的结果（DataFrame）并返回带有schema的`BaseRelation`
- `RelationProvider` 创建接口
  - 接收用户的设置参数，创建`BaseRelation`
- `SchemaRelationProvider` 通过给定参数和用户定义的Schema创建`BaseRelation`
  - 需要用户定义的schema
- `BaseRelation` 抽象类，作为逻辑计划中使用的数据源的表示
  - 提供数据的schema信息、SQL上下文信息
  - 各个数据源，需要继承该类，作为其数据源表在spark中的表示
- `TableScan`  读数据接口
  - 配合`BaseRelation` ，返回行迭代的RDD[Row]
  - 其他`PrunedFilteredScan` 支持filter，列裁剪
  - 该接口被`DataSourceStrategy` 的`apply`方法调用，做filter，列裁剪功能
- `InsertableRelation` 写数据的接口
  - 接受DataFrame参数，写到数据源
- 流相关接口
  - `StreamSinkProvider`
    - 流接收器提供者，用于结构化流
  - `StreamSourceProvider`
    - 流数据源提供者，用于结构化流



DataSource

- 创建
  - 使用需要使用别名或者完全限定的类名（完整类名）来加载类
    - 别名需要实现`DataSourceRegister` trait
  - 需要`SparkSession` 提供配置信息，来解析数据源provider
  - 数据路径列表（默认是空）
    - 不同数据源，是不同的
      - Hive表，是uri
      - mysql表，是表名
- 被使用的地方
  - `HiveMetastoreCatalog` 转换`HiveTableRelation`为 `LogicalRelation`
    - 实际转换为`HadoopFsRelation`
  - `DataFrameReader` 装载一个数据源
    - 通过`SparkSession.read`方法获取reader对象
  - `DataFrameWriter`写入到一个数据源
    - `DataFrameWriter`是一个以批处理方式将[数据集](https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-Dataset.html)持久化到外部存储系统的接口。
    - 通过`DataSet.write`方法获取writer对象
  - `CreateDataSourceTableCommand` 等命令执行时
- 内置Datasource API的实现
  - jdbc jdbc数据源，可以算是最基本通用的方式连接其他数据库，其他数据库只要支持jdbc，就能接入spark，但是jdbc连接性能不行（单点查询），无法支持大规模数据，还是需要通过自己实现的Datasource接口获得更好的性能。
    - 检查3.0版本源码，允许提供一些分区信息，来生成分区，对此有所改进
    - jdbc内置，支持的数据库，mysql，db2，mariadb，pg，orcacle，mssql
    - 关键实现类
      - `JDBCRelation` 继承`BaseRelation`,实现`PrunedFilteredScan`, `InsertableRelation` 接口
        - 提供schema信息
        - 支持对jdbc表的读、写
          - 读返回的RDD是`JDBCRDD`
            - 包含schema，要读取的列，filter信息，url信息，jdbc参数，分区
            - 执行依赖`JdbcUtils` 提供的方法，对jdbc连接的数据库进行查询
      - `JdbcRelationProvider` 实现`CreatableRelationProvider`,`RelationProvider`,`DataSourceRegister` 接口
        - 支持根据DF创建jdbc表，即将DF保存
        - 支持根据指定参数，构造jdbc表
      - `JdbcUtils` 工具类，通过jdbc连接，执行一些ddl，dml操作
  - hive(hadoop fs表)
  - kafka
  - 官方demo：`SimpleScanSource`



### 3.2 DataSource V2

[SPARK-25186](https://issues.apache.org/jira/browse/SPARK-25186)





### 3.3 Spark on K8S







## REF

- [Spark底层执行原理详细解析](https://mp.weixin.qq.com/s/qotI36Kx3nOINKHdOEf6nQ)
- High performance spark 
- [如何在 Kyuubi 中使用 Spark 自适应查询执行 (AQE)](https://kyuubi.readthedocs.io/en/latest/deployment/spark/aqe.html)
- [自适应查询执行：在运行时加速 Spark SQL](https://databricks.com/blog/2020/05/29/adaptive-query-execution-speeding-up-spark-sql-at-runtime.html)
- [slides:Scaling your Data Pipelines with Apache Spark on Kubernetes](https://www.slideshare.net/databricks/scaling-your-data-pipelines-with-apache-spark-on-kubernetes)
- [slides:Spark on Kubernetes - Advanced Spark and Tensorflow Meetup - Jan 19 2017 - Anirudh Ramanthan from Google Kubernetes Team](https://www.slideshare.net/cfregly/spark-on-kubernetes-advanced-spark-and-tensorflow-meetup-jan-19-2017-anirudh-ramanthan-from-google-kubernetes-team)
- [slides:Apache Spark on Kubernetes Anirudh Ramanathan and Tim Chen](https://www.slideshare.net/databricks/apache-spark-on-kubernetes-anirudh-ramanathan-and-tim-chen)
- [slides:Spark day 2017 - Spark on Kubernetes](https://www.slideshare.net/jerryjung7/spark-day-2017seoul)
- [spark datasource](https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-DataSource.html) datasource 接口说明
- [spark官方datasource 使用教程](https://spark.apache.org/docs/latest/sql-data-sources.html)
- [slides:Data Source API in Spark](https://www.slideshare.net/databricks/yin-huai-20150325meetupwithdemos)datasource api主要开发者的slide
- [slides:Anatomy of Data Source API : A deep dive into Spark Data source API](https://www.slideshare.net/datamantra/anatomy-of-data-source-api) CSV具体示例
- [slides:spark sql-2017](https://www.slideshare.net/joudkhattab/spark-sql-77435155)
- [slides:Intro to Spark and SparkSQL-2014](https://cseweb.ucsd.edu/classes/fa19/cse232-a/slides/Topic7-SparkSQL.pdf)
- [slides:A Deep Dive into Query Execution Engine of Spark SQL-2019](https://www.slideshare.net/databricks/a-deep-dive-into-query-execution-engine-of-spark-sql)  WSCG
- [slides:A Deep Dive into Spark SQL's Catalyst Optimizer with Yin Huai-2017](https://www.slideshare.net/databricks/a-deep-dive-into-spark-sqls-catalyst-optimizer-with-yin-huai)
- [slides:Understanding Query Plans and Spark UIs-2019](https://www.slideshare.net/databricks/understanding-query-plans-and-spark-uis)


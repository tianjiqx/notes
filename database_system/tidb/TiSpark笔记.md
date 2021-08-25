# TiSpark笔记

## 1. 背景

正如在TiDB原理提到，TiSpark为了提升OLAP能力，而引入，同时将TiDB也接入了Spark生态。

TiSpark实际上继承Spark的DataSource接口，来支持Spark读取TiKV的数据。实际是一个driver。



## 2. 架构

![](tidb图片/tispark-architecture.png)

- Spark集群
  - 通过TiSpark **事务**的读/写取TiKV数据
- TiKV集群
  - 存储集群
- PD集群
  - TiSpark 获取region信息
- TiDB集群（可选）
  - 为了保证多写（tidb写）一致性，需要加表锁，应该是必选





源码版本2021.05.31：

6eb662cf12744741478ce8a97eb8b00af003beac



源码结构：

- core
  - datasource接口实现相关，完成写功能
  - Spark Strategy 和 Spark Optimizer接口hook sparkSQL的优化器和物理执行计划生成，完成数据的读的优化
    - 可以转换为索引访问的，谓词
    - 计算下推（filter），计算key range
      - 聚合下推，avg 改写为 sum/count
    - 基于代价的 join reorder
    - Data location，数据本地化
      - 与PD沟通获取
- tikv-client
  - 是一个完整的 TiKV 的独立的 Java 实现的接口，负责解析对 TiKV 进行读取和数据解析，谓词处理等等
    - 不需要管spark接口的变更，不用担心spark升级产生兼容性问题
  - 与TIDB、TIKV集群通信的客户端（基于gRPC）
  - 与PD通信，请求region
  - 与TiKV通信，读写数据，结果数据的SerDe
  - 计算下推到coprocessor
- tipb （构建后自动生成）
  - protobuf 定义生成的文件



## 3.实现

### 3.1 执行环境

执行环境TiContext 是对SparkSession的包装，持有关键的TiSession和TiSessionCatalog

- `com.pingcap.tikv.TiSession`
  - 维持与TiKV、PD通信的会话信息。缓存Catalog，region元信息。
    - `com.pingcap.tikv.region.RegionManager`
      - `com.pingcap.tikv.region.RegionCache` region缓存管理器
        - `com.pingcap.tikv.PDClient`  PD 客户端
      - `com.pingcap.tikv.catalog.Catalog` 数据库、表信息
        - `com.pingcap.tikv.catalog.CatalogCache`
  - 获取PD全局唯一时间戳
    - `com.pingcap.tikv.PDClient` 
  - tikv事务客户端
    - `com.pingcap.tikv.txn.TxnKVClient` 用于写数据时，2阶段提交
  - 获取索引扫描，表扫描的全局工作线程池
    - `com.pingcap.tikv.operation.iterator.ScanIterator`
    - `com.pingcap.tikv.operation.iterator.IndexScanIterator`
      - Future 异步IO模式？
- `org.apache.spark.sql.catalyst.catalog.TiSessionCatalog` 
  - TiCompositeSessionCatalog ddl操作，sparkSQL的 `SessionCatalog` 扩展接口的实现
  - 子类`org.apache.spark.sql.catalyst.catalog.TiCompositeSessionCatalog`
    - 继承sparkSQL的`SessionCatalog` 类型
    - 组合spark 和 tidb的 Catalog信息，完整的给spark使用的SessionCatalog。
  - 子类`org.apache.spark.sql.catalyst.catalog.TiConcreteSessionCatalog` tidb的Catalog信息
    - 继承sparkSQL的`SessionCatalog` 类型，该类的说明，见[spark笔记](https://github.com/tianjiqx/notes/blob/master/big_data_system/spark/Spark%E7%AC%94%E8%AE%B0.md)2.2.2 catalog 节
    - `org.apache.spark.sql.catalyst.catalog.TiDirectExternalCatalog` 成员
      - 继承sparksql `ExternalCatalog`, sparkSQL外接注册的catalog信息
      - 关键成员 `com.pingcap.tispark.MetaManager` 获取tidb数据库、表
        - 包装`com.pingcap.tikv.catalog.Catalog`

### 3.2 元信息

`org.apache.spark.sql.TiExtensions`

- 继承sparksql的`SparkSessionExtensions`
- 用于注册spark 计划生成（catalyst）的扩展
  - 配置文件需要设置conf:`spark.sql.extensions org.apache.spark.sql.TiExtensions `
- 扩展
  - `org.apache.spark.sql.extensions.TiParser`
  - `org.apache.spark.sql.extensions.TiDDLRule`
  - `org.apache.spark.sql.extensions.TiResolutionRuleV2` 逻辑优化
  - `org.apache.spark.sql.TiStrategy` 逻辑计划转物理计划的策略
    - 将`com.pingcap.tispark.TiDBRelation`  转换成`SparkPlan`
      - 这一步会生成`com.pingcap.tikv.meta.TiDAGRequest` 对象
  - `org.apache.spark.sql.catalyst.expressions.TiBasicExpression`
    - spark表达式转换tidb表达式

`org.apache.spark.sql.catalyst.catalog.TiCatalog ` 

- 继承spark `TableCatalog`,`SupportsNamespaces` 接口
  - spark 3.0 的Catalog接口
- 底层依然使用`com.pingcap.tispark.MetaManager` 获取tidb数据库、表



`com.pingcap.tispark.TiDBDataSource` 

- 写数据
- 实现了`DataSourceRegister`,`RelationProvider`,`SchemaRelationProvider`,`CreatableRelationProvider`接口
  - 提供别名
  - 根据参数，创建`TiDBRelation`
  - 根据用户定义的Schema创建`TiDBRelation`
  - 根据DF，保存数据并创建`TiDBRelation`

`com.pingcap.tispark.TiDBRelation`

- 逻辑查询计划，表示一张表
- 继承`BaseRelation`，实现`InsertableRelation`接口
  - 支持将DF写入TiDB(实际TiKV)
    - `TiDBWriter.write()`

### 3.3 读

- `com.pingcap.tikv.meta.TiDAGRequest` TiKV 读取数据请求
  - TypeTableScan
  - TypeIndexScan
  - TypeSelection
  - TypeAggregation
  - TypeTopN
  - TypeLimit

- `com.pingcap.tikv.operation.iterator.DAGIterator<T>` 继承 `CoprocessorIterator<T>`
  - 根据`DAGRequest` 迭代数据 （同TiDB 的Select API模型，可参考tidb原理笔记）
    - 根据`RegionTask` 读取region数据
    - `com.pingcap.tidb.tipb.SelectResponse`  单个region的响应，会存储在`com.pingcap.tidb.tipb.Chunk` 
  - `com.pingcap.tikv.row.DefaultRowReader ` 继承`RowReader` 
    - `Row readRow(DataType[] dataTypes)` 根据row的类型，从输入流中，解析row对象每个一列值
      - `com.pingcap.tikv.codec.CodecDataInput` 输入流



### 3.4 写

TiDBWriter

- 表是否存在的检查，通过jdbc 接口查询TiDB集群
- `TiBatchWrite.write` 将DataFrame批量追加到TiDB
  - 使用jdbc接口，加表锁，释放表锁，更新统计信息
    - 锁表，为了避免tispark事务冲突，产生大量回滚
  - `preCalculate`  
    - `sparkRow2TiKVRow`将spark row转为tikv的row
      - 具体类型转换实现在tikv-client的`DataType`实现类中将java对象转换为TiDB的使用的java对象类型（MySQL）
    - 生成rowID
  - 待写数据RDD切分region
    - 预先切分region，避免热点写，和region分裂
  - **挑选primarykey， percolator模型2pc提交**



Spark的DataFrame是针对单表概念，只能完成单表的事务ACID。

对于多表的事务写，Tispark给出的方案是，将多表融合成一个DataFrame进行写。

提供额外的接口:

```scala
def write(
    dataToWrite: Map[DBTable, DataFrame], // 待写入的多表
    sparkSession: SparkSession,
    parameters: Map[String, String]): Unit 
```

整个最终的DataFrame，并不是以传统的单表column关系组织，而是KV的集合。最后通过`TiBatchWrite.write` 写入时，没一行实际都是一个KV，并不特定的写某张表，所以，能够保证对多表的写入，也可以使用2阶段提交的方式，对多表进行写入。



## REF

- [Giithub:TiSpark](https://github.com/pingcap/tispark)
- [演讲实录|马晓宇：When TiDB Meets Spark](https://zhuanlan.zhihu.com/p/29052313)
- [基于 TiSpark 的海量数据批量处理技术](https://zhuanlan.zhihu.com/p/264173698)


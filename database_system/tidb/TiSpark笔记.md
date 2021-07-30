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
  - datasource接口实现相关
- tikv-client
  - 与TIDB、TIKV集群通信的客户端（基于gRPC）
  - 与PD通信，请求region
  - 与TiKV通信，读写数据，结果数据的SerDe
  - 计算下推到coprocessor
- tipb （构建后自动生成）
  - protobuf 定义生成的文件



## 3.实现



### 3.1 执行环境

执行环境TiContext 是对SparkSession的包装，持有关键的TiSession和TiSessionCatalog

- TiSession
  - 维持与TiKV、PD通信的会话信息。缓存Catalog，region元信息。
- TiSessionCatalog
  - TiCompositeSessionCatalog ddl操作，spark SessionCatalog 接口实现





### 3.2 元信息

TiSessionCatalog

TiCatalog 继承spark TableCatalog，具体DDL实现。

TiDBDataSource spark的DefaultSource tidb数据源，提供BaseRelation表对象。

定义TiDBRelation





### 3.3 读



### 3.4 写

TiDBWriter

- 表是否存在的检查，通过jdbc 接口查询TiDB集群
- `TiBatchWrite.write` 将DataFrame批量追加到TiDB
  - 使用jdbc接口，加表锁，释放表锁，更新统计信息
  - `preCalculate`  
    - 将spark row转为tikv的row
    - 生成rowID
  - 待写数据RDD切分region
  - **挑选primarykey， percolator模型2pc提交**

### 3.5 事务





## REF

- [Giithub:TiSpark](https://github.com/pingcap/tispark)


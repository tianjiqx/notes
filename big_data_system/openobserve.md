## OpenObserve

OpenObserve（简称O2）是一个云原生的可观察性平台，专为日志、指标、跟踪、分析、RUM（真实的用户监控-性能、错误、会话回放）而构建，旨在以PB级规模工作。

Features:

- Logs, Metrics, Traces 支持
- OpenTelemetry Support 完全兼容
- Alerts & Dashboards
- SQL and PromQL Support
- 单一二进制安装
  - 确实单个服务安装很快
- 多功能存储选项：支持本地磁盘，S3，MinIO，GCS，Azure Blob存储。
- Dynamic Schema

## 原理

### 架构

- 元信息服务
  - local 的 sqllite
  - postgres、mysql 主备
- 

### 写入

![ingester](https://openobserve.ai/docs/images/arch-sequence-ingester.svg)

- 从HTTP / gRPC API请求接收数据。
  
  > 解析：

- 逐行解析数据

- 检查是否有任何函数（摄取函数）用于转换数据，按函数顺序调用每个摄取函数

- 检查时间戳字段，将时间戳转换为微秒;如果记录中没有时间戳字段，则设置当前时间戳。

- 检查流模式以确定schema是否需要演化。在这里，如果我们发现架构需要更新以添加新字段或更改现有字段的数据类型，则获取 lock 以更新schema。

- 评估真实的实时警报（如果为流定义了任何警报）。
  
  > : 写入

- 按时间戳在每小时的桶中写入WAL文件，然后将请求中的记录转换为Arrow RecordBatch并写入Memtable。
  
  - 根据 organization/stream_type 创建Memtable，如果仅为 logs 摄取数据，则只有一个Memtable
  - WAL文件和Metable是成对创建的，一个WAL文件有一个Memtable。WAL文件位于 data/wal/logs 。

- 当Memtable大小达到 ZO_MAX_FILE_SIZE_IN_MEMORY=256 MB或WAL文件达到 ZO_MAX_FILE_SIZE_ON_DISK=128 MB时，我们将Memtable移动到Immutable并创建一个新的Memtable & WAL文件用于写入数据。

- 每隔 ZO_MEM_PERSIST_INTERVAL=5 秒将把Immutable转储到本地磁盘。一个Immutable将导致多个parquet文件，因为它可能包含多个流和多个分区，parquet文件位于 data/wal/files 。

- 每隔 ZO_FILE_PUSH_INTERVAL=10 秒，我们检查本地拼花文件，如果任何分区的总大小超过 ZO_MAX_FILE_SIZE_ON_DISK=128 MB或任何文件已 ZO_MAX_FILE_RETENTION_TIME=600 秒前，所有这样的小文件在一个分区将合并成一个大文件（每个大文件将最大 ZO_COMPACT_MAX_FILE_SIZE=256 MB），这将被移动到对象存储。


高可用问题：
- 只有 meta（PG） HA 备份
- 存在 WAL，并且数据存放S3 保证，持久化数据可以不丢，但是似乎无日志多副本机制，存在单机崩溃，磁盘损坏，丢失新数据问题



### 查询

Querier 查询器

查询器用于查询数据。Queriers节点是完全无状态的。

![query](https://openobserve.ai/docs/images/arch-sequence-querier.svg)

- 使用http API接收搜索请求。接收查询请求的节点变为 LEADER querier for the query 。其他查询器是 WORKER queriers for query 。
- LEADER 解析并验证SQL。
- LEADER 查找数据时间范围，从文件列表索引中获取文件列表。
- LEADER 从集群元数据中获取查询器节点。
- LEADER 每个查询器要查询的文件的分区列表。例如，如果需要查询100个文件，并且有5个查询器节点，则每个查询器可以查询20个文件， LEADER 处理20个文件， 每个 WORKERS 处理20个文件。
- LEADER 调用运行在每个 WORKER 查询器上的gRPC服务，将搜索查询调度到查询器节点。查询器之间的通信使用gRPC进行。
- LEADER 收集、合并并将结果发送回用户。

优化：

- 默认情况下，查询器将在内存中缓存parquet文件。您可以使用环境变量 ZO_MEMORY_CACHE_MAX_SIZE 配置查询器用于缓存的内存量。默认缓存是用特定查询器可用内存的50%来完成的。
- 在分布式环境中，每个查询节点只缓存一部分数据。
- 我们还可以选择在内存中缓存最新的parquet文件。当摄取器生成一个新的parquet文件并将其上传到对象存储时，摄取器将通知查询器缓存该文件。

#### Federated Search 联合搜索

联合搜索跨越多个OpenObserve集群：

- 在其中一个集群上接收搜索请求，接收查询请求的节点称为 LEADER cluster for the query 。其他集群是 WORKER clusters for that query 。
- LEADER cluster 使用超级集群元数据查找所有集群。
- LEADER cluster 在每个 WORKER cluster 上调用gRPC服务，使用相同的查询负载作为输入。
- WORKER cluster 如上所述执行查询，其中一个节点成为每个集群中的 LEADER querier ，并调用同一集群中的其他 WORKER queriers ，来自所有工作者和领导者的结果由 LEADER cluster 合并。
- LEADER cluster 收集、合并并将结果发送回用户。

## 测试

HDFS
|                             | 存储空间           | load time |
|-----------------------------|-------------------------|-----------|
| openobserve 25,821,184      | 375.80 MB                 | 916       |
| doris（lz4）82293702行(3.18X) | 2.263 GB(/3.18=728.7MB) | 54.248    |

压缩效果更好？ 似乎默认是zstd 压缩 （write_file_list_s3）

TSBS

| 表   | 存储空间（MB）  | doris（MB） | ck（MB） |
| --- | --------- | --------- | ------ |
| cpu | 106.56 MB | 70.401    | 130    |

## REF

- [architecture](https://openobserve.ai/docs/architecture/)
- [github:openobserve](https://github.com/openobserve/openobserve)
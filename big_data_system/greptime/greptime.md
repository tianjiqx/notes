# GreptimeDB

## 架构

![](./images/architecture.jpg)

共享存储架构

- MetaServer集群(可选)
    - 存储和管理整个GreptimeDB集群的元数据，包括节点Meta信息（IP地址、端口、角色等），表的地址信息（区域和分布）、表的Meta信息（模式、选项等）集群状态管理（节点状态、各种全局状态、全局任务状态等）
- 前端集群
    - 作为代理和路由器，根据表的位置信息和负载均衡规则将读写请求路由到正确的后端节点
    - 承担了跨区域或跨表的分布式查询功能
    - 无状态
- Datanode集群
    - 处理读/写请求
    - 配置和角色分布到不同的计算能力池：读、写，分析，计算节点
        - Python co-processor: python 协处理器
        - Storage engine：Mito
            - 基于LSM树的时间序列数据表引擎
        - Query engine： datafusion
        - 每个函数都可以作为一个特定的计算池Datanode Computation pool 单独启动，并且读取，写入，分析和Python计算的负载可以隔离而不会相互影响
- Remote storage 远程存储(可选)
    - 数据和日志将存储在ObjectStore中（基于OpenDAL项目）
    - 将“冷”数据存储在S3中，将“热”数据存储在本地磁盘中
    - 共享的分布式WAL只需要少量的EBS来提供写容灾，在数据刷新到S3后即可清空


![](./images/architecture-3.png)

Storage engine：
![](./images/overall-achitecture.jpg)

- 数据首先写入WAL和memtable，然后当memtable中的数据达到某个阈值时，以Parquet格式持久化到级别0。这些文件可以存储在对象存储中
- Compaction
    - 按时间范围对文件进行分区，以便轻松实现TTL
    - 为parquet文件建立额外索引以提高查询效率


#### 智能索引

在时间序列的分析场景中，最常见的查询模式是根据给定的标签和时间范围来定位拟合序列。

传统：
- InfluxDB使用倒排索引， 当序列号增加时，最终会将内存溢出到磁盘
- MPP，并行加速

GreptimeDB混合的解决方案-构建智能索引和大规模并行处理（MPP）来增强修剪和过滤

独立的索引文件来记录统计信息，MinMax，Dictionary，Bloomfilter索引
![](./images/index-file-structure.png)

通过内置的指标记录不同查询的工作负载，智能应用索引


#### 压缩

B在块的基数超过某个阈值时对字符串进行字典化

浮点数，GreptimeDB采用Chimp算法（增强版Gorilla）

Serverless 后台 异步Compaction


## 数据模型

![](./images/time-series-data-model.svg)

- 表模型 + Schema 版本

- SQL

- 多值模型使其中一行数据可以具有多个指标列, 共用tag


GreptimeDB 如何解决高基数问题？（各自实现不同，高基数具体的问题）

- 分片：它将数据和索引分布在不同的 Region 服务器之间。阅读 GreptimeDB 的架构。
- 智能索引：它不强制为每个标签创建倒排索引，而是根据标签列的特性和负载类型选择合适的索引类型并自动构建
    - 认为所有tag都构建倒排，开销太大，而且异步构建
- MPP: 除了索引之外，查询引擎还会利用向量化执行和分布式并行执行等技术来加速查询。



## REF

- [GreptimeTeam/greptimedb](https://github.com/GreptimeTeam/greptimedb)

- [docs: datanode/overview](https://docs.greptime.com/contributor-guide/datanode/overview)


- [2022-12-08-GreptimeDB-internal-design](https://greptime.com/blogs/2022-12-08-GreptimeDB-internal-design)

- [GreptimeDB存储引擎设计-迎合时间序列场景](https://greptime.com/blogs/2022-12-21-storage-engine-design)
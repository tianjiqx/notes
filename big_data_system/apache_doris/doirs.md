
# Apache Doris

## 背景
Apache Doris 系列，官方商业公司 selectdb，分叉版本starrocks。 



## 数据模型

doris [数据模型](https://doris.apache.org/zh-CN/docs/table-design/data-model/overview) 应该参考了 ck 的 MergeTree 系列的设计。

Doris 的数据模型主要分为3类:

- 聚合模型 Aggregate
- 主键模型 Unique
- 明细模型 Duplicate

### Unique
当用户有数据更新需求时，可以选择使用主键数据模型（Unique）。

- 读时合并 (merge-on-read)。在读时合并实现中，用户在进行数据写入时不会触发任何数据去重相关的操作，所有数据去重的操作都在查询或者 compaction 时进行。因此，读时合并的写入性能较好，查询性能较差，同时内存消耗也较高。
- 写时合并 (merge-on-write)。在 1.2 版本中，我们引入了写时合并实现，该实现会在数据写入阶段完成所有数据去重的工作，因此能够提供非常好的查询性能。自 2.0 版本起，写时合并已经非常成熟稳定，由于其优秀的查询性能，我们推荐大部分用户选择该实现。自 2.1 版本，写时合并成为 Unique 模型的默认实现。



### Duplicate
在某些多维分析场景下，数据既没有主键，也没有聚合需求。针对这种需求，可以使用明细数据模型。

DUPLICATE KEY，只是用来指明数据存储按照哪些列进行排序。

时间序列数据，比如日志、指标等

### Aggregate

Aggregate 表中的列按照是否设置了 AggregationType，分为 Key (维度列) 和 Value（指标列）。没有设置 AggregationType 的 user_id、date、age、sex 称为 Key，而设置了 AggregationType 的称为 Value。
Doris 中指标列，最终只会存储聚合后的数据，丢失明细数据。


几种聚合方式和 agg_state：

- SUM：求和，多行的 Value 进行累加。
- REPLACE：替代，下一批数据中的 Value 会替换之前导入过的行中的 Value。
- MAX：保留最大值。
- MIN：保留最小值。
- REPLACE_IF_NOT_NULL：非空值替换。和 REPLACE 的区别在于对于 null 值，不做替换。
- HLL_UNION：HLL 类型的列的聚合方式，通过 HyperLogLog 算法聚合。
- BITMAP_UNION：BIMTAP 类型的列的聚合方式，进行位图的并集聚合。


## REF

- [Apache Doris 用于网易中的日志和时间序列数据分析，为什么不是 Elasticsearch 和 InfluxDB](https://doris.apache.org/blog/apache-doris-for-log-and-time-series-data-analysis-in-netease/)
    - es 日志 -> 70% 的存储成本降低和 11 倍查询速度提升
    - InfluxDB 指标 -> 存储成本降低 67% , 机器（cpu） 50 %， 查询性能也基本更好
- [From Elasticsearch to Apache Doris: upgrading an observability platform](https://doris.apache.org/blog/from-elasticsearch-to-apache-doris-upgrading-an-observability-platform/)
    - 存储成本降低 70%，查询速度(比es)提高 300%
    - 查询2路径：
        - 如果 Doris 支持查询 SQL 语义或函数，Guance-Select 会将查询下推到 Doris 前端进行计算
        - 通过 Thrift RPC 接口获取 Arrow 格式的列式数据，然后在 Guance-Select 中完成计算
    - Variant 数据类型支持dynamic schema change

- [Apache Doris 迎来重磅升级！云原生存算分离架构来了](https://www.infoq.cn/article/u9x7rwcqvkeq2ptbmm3n)


- [selectdb 文档、ppt汇总](https://selectdb.feishu.cn/docx/doxcnm0uTBWFTc4Qn9A1WHuqrcg)


- [StarRocks 源码解析](https://www.zhihu.com/column/c_1595736761170358272)

- [Apache Doris 入门 10 问](https://cloud.tencent.com/developer/article/2378217) RowSet 概念

- [Doris存储文件格式优化](https://doris.apache.org/zh-CN/community/design/doris_storage_optimization)
    - Doris 0.12 版本中实现了新的存储格式：Segment V2，引入词典压缩、bitmap索引、page cache等优化，能够提升系统性能。
- [Doris 存储层设计介绍 1——存储结构设计解析（索引底层结构）](https://blog.csdn.net/SHWAITME/article/details/136155008) 推荐


- [合集·《Apache Doris 源码阅读与解析》 系列直播](https://space.bilibili.com/362350065/channel/collectiondetail?sid=296007) bilibili

- [BE存储引擎部分代码设计文档(2019)](https://wingsgo.github.io/2020/02/24/doris-03-be_refactor_2019.html)
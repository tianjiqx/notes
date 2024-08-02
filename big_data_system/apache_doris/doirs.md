
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


## 索引支持

- [前缀索引](https://doris.apache.org/zh-CN/docs/2.0/table-design/index/prefix-index) (类似二级索引，但是要求顺序)
- bitmap [位图索引](https://www.inlighting.org/archives/what-is-bitmap-indexing) 低基数 多条件过滤
- [倒排索引](https://doris.apache.org/zh-CN/docs/2.0/table-design/index/inverted-index)
- [BloomFilter 索引](https://doris.apache.org/zh-CN/docs/dev/table-design/index/bloomfilter) 跳数索引
- [NGram BloomFilter ](https://doris.apache.org/zh-CN/docs/dev/table-design/index/ngram-bloomfilter-index) 基于 BloomFilter 的跳数索引， 为 like 语句


## 编码
```
enum EncodingTypePB {
    UNKNOWN_ENCODING = 0;
    DEFAULT_ENCODING = 1;
    PLAIN_ENCODING = 2;
    PREFIX_ENCODING = 3;
    RLE = 4;
    DICT_ENCODING = 5;
    BIT_SHUFFLE = 6;
    FOR_ENCODING = 7; // Frame-Of-Reference
}
```



根据 EncodingInfoResolver 构造函数 _add_map 定义顺序，第一次出现的 FieldType 添加的是默认值，可得出 各类型的默认编码方式


| Column Type     | Supported Encoding Methods      | Default Encoding Method |
|-----------------|---------------------------------|-------------------------|
| TINYINT         | Bit Shuffle, Plain,FOR_ENCODING | Bit Shuffle             |
| SMALLINT        | Bit Shuffle, Plain,FOR_ENCODING | Bit Shuffle             |
| INT             | Bit Shuffle, Plain,FOR_ENCODING | Bit Shuffle             |
| BIGINT          | Bit Shuffle, Plain,FOR_ENCODING | Bit Shuffle             |
| UNSIGNED BIGINT | Bit Shuffle                     | Bit Shuffle             |
| UNSIGNED INT    | Bit Shuffle                     | Bit Shuffle             |
| LARGEINT        | Bit Shuffle, Plain,FOR_ENCODING | Bit Shuffle             |
| FLOAT           | Bit Shuffle, Plain              | Bit Shuffle             |
| DOUBLE          | Bit Shuffle, Plain              | Bit Shuffle             |
| CHAR            | Dictionary, Plain, Prefix       | Dictionary              |
| VARCHAR         | Dictionary, Plain, Prefix       | Dictionary              |
| STRING          | Dictionary, Plain, Prefix       | Dictionary              |
| JSONB           | Dictionary, Plain, Prefix       | Dictionary              |
| VARIANT         | Dictionary, Plain, Prefix       | Dictionary              |
| BOOL            | Run Length, Bit Shuffle, Plain  | Run Length              |
| DATE            | Bit Shuffle, Plain              | Bit Shuffle             |
| DATEV2          | Bit Shuffle, Plain              | Bit Shuffle             |
| DATETIMEV2      | Bit Shuffle, Plain              | Bit Shuffle             |
| DATETIME        | Bit Shuffle, Plain              | Bit Shuffle             |
| DECIMAL         | Bit Shuffle, Plain              | Bit Shuffle             |
| DECIMAL32       | Bit Shuffle, Plain              | Bit Shuffle             |
| DECIMAL64       | Bit Shuffle, Plain              | Bit Shuffle             |
| DECIMAL128I     | Bit Shuffle, Plain              | Bit Shuffle             |
| DECIMAL256      | Bit Shuffle, Plain              | Bit Shuffle             |
| IPV4            | Bit Shuffle, Plain              | Bit Shuffle             |
| IPV6            | Bit Shuffle, Plain              | Bit Shuffle             |
| HLL             | Plain                           | Plain                   |
| OBJECT          | Plain                           | Plain                   |
| QUANTILE_STATE  | Plain                           | Plain                   |
| AGG_STATE       | Plain                           | Plain                   |


[CREATE-TABLE](https://doris.apache.org/zh-CN/docs/dev/sql-manual/sql-statements/Data-Definition-Statements/Create/CREATE-TABLE) 中未找到如何定义列的codingType 语法，也许是todo状态

## 存算分离

- 冷热数据分层，实现冷数据存储分离
    - 热数据本地 Cache，全量数据在对象存储
    - 云磁盘的价格通常是对象存储的 5-10 倍，如果可以将 80% 的冷数据保存到对象存储中，存储成本至少可降低 70% ;
- 弹性计算节点，实现计算分离，无状态

- 独立的读集群，读取S3数据

主要的问题：实时性无法保证


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

- [Doris 实现原理之高效存取 varchar 字符串](https://cloud.baidu.com/article/3319774) 推荐
    - 字典编码,plain 编码 存储 字典页
        - Doris 采用的是试探法，优先先采用字典编码，随着数据增加， 如果字典大小超过一定的阈值退回 plan 编码，目前这个阈值是 dict_page 大小超过 64KB
    - 数字优化：引入 Bitshuffle 算法来对数字按照 bit 重新进行打散排序 提高 lz4 压缩效率
        - Bitshuffle 重新排列一组值以存储每个值的最高有效位，其次是每个值的第二个最高有效位，依此类推。

    - [字符串编码/解码](https://www.cnblogs.com/bitetheddddt/p/15210062.html)
        - 字典编码+bitshuffle+lz4压缩

    -  根据 [pr](https://github.com/apache/doris/pull/1304) 应当是参考了 kudu 的 bitshuffle 实现
    - EncodingInfoResolver 类定义的各类型支持编码方式

- [文本检索性能提升 40 倍，Apache Doris 倒排索引深度解读](https://selectdb.com/blog/158)
    - 倒排索引: 
        - 大规模数据非主键列点查场景
        - 短文本分布比较集中（如大量文本相似，少量文本不同）
        - 长文本列的文本搜索场景
    - Ngram Bloom Filter 索引: like 场景，短文本分布比较离散（即文本之间相似度低）
- [Apache Doris 如何基于自增列满足高效字典编码等典型场景需求](https://selectdb.com/blog/194)

- [Apache Doris 巨大飞跃：存算分离新架构](https://selectdb.com/blog/101)
    - 基于共享存储系统的主数据存储(HDFS/对象存储)
    - 基于本地高速缓存的性能优化
        - 缓存系统替代原来的节点内存储系统（mem？disk cache）
    - 多计算集群实现工作负载隔离
        - 物理隔离，snowflake vm


- [StarRocks 完美开发环境搭建](https://www.inlighting.org/archives/setup-perfect-starrocks-dev-env)

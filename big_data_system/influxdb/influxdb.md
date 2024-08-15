# InfluxDB

influxdb 是目前最出名的开源的时间序列数据库。

## schema 设计

InfluxDB数据模型将时间序列数据组织到桶buckets和度量measurements中。一个桶可以包含多个度量。测量包含多个tag和field。

- Bucket 桶：存储时间序列数据的命名位置。在InfluxDB SQL实现中，存储桶与数据库同义。一个桶可以包含多个度量。
    - Measurement 测量：时间序列数据的逻辑分组。在InfluxDB SQL实现中，度量与表同义。给定测量中的所有点都应具有相同的tag。测量包含多个tag和field。需要注意测量不是一个指标，而是一类，field才代表一个具体指标。比如cpu测量，下面usr，idle，sys是指标。由于共享tag，所以一般一起存储。
        - Tags 标签：存储每个点的元数据字符串值的键值对，例如，标识或区分数据源或上下文的值，例如主机、位置、工作站等。tag值可以为空。
        - Fields 字段：存储每个点的数据的键值对，例如温度、压力、股票价格等。字段值可以为空，但在任何给定行上至少有一个字段值不为空。
        - Timestamp 时间戳：与数据关联的时间戳。当存储在磁盘上并进行查询时，所有数据都按时间排序。在InfluxDB中，时间戳是UTC中的纳秒级Unix时间戳。
    - 主键
      - 行的主键是点的时间戳和tag集的组合-tag keys和tag values的集合

什么应该是标记，什么应该是字段？
- 使用标记来存储元数据，或有关数据源或上下文的标识信息。
- 使用字段存储测量值。
- tag值只能是字符串。
- 字段值可以是以下任何数据类型：
  - Integer，Unsigned integer ，Float，String，Boolean


索引
- 不索引tag values或 fields value
  - 不对 values进行索引，所以支持无限基数？
- 索引 tag keys， fields keys和其他元数据

> InfluxDB v3存储引擎支持无限tag values和series cardinality。与TSM存储引擎支持的InfluxDB不同，标记值基数不会影响数据库的整体性能。



## 实践

- 避免宽模式 （本身也不允许超过250列）
  - 宽模式是一个具有许多tag和字段以及每个tag和字段对应的列的模式。
    - InfluxDB v3是一个列式数据库，宽模式不影响查询性能
    - 影响：
      - 在摄取期间持久化和压缩数据需要更多资源
      - 由于包含太多tag的复杂主键，导致排序性能下降
  - 超过249个tag和字段，考虑将字段分割为单独的度量

- 避免过多的标签
  - 行的主键是点的时间戳和tag集的组合-tag keys和tag values的集合。包含更多tag的点具有更复杂的主键，如果使用键的所有部分进行排序，则可能会影响排序性能。

-  不应将多个属性（位置、型号和ID）放到一个tag中，而是使用单独tag，避免查询复杂（使用like，正则）

## 关键设计

###  时间序列数据的属性

- 数十亿个独立数据点
- 高写入吞吐量
- 高速取吞吐量
- 大量删除 (过期数据)
- 主要是插入/附加工作负载，很少更新

### 高基数（Cardinality）问题
高基数（Cardinality）问题是指在时序数据库中，标签（tag）的数量过多，导致每个数据点都有大量不同的标签组合，这种现象称为时间线膨胀（time series cardinality explosion）。这对TSM（Time-Structured Merge Tree）存储引擎的影响主要体现在以下几个方面：

- 索引性能下降：TSM存储引擎依赖于时间序列的倒排索引来快速检索数据。当存在高基数问题时，索引的大小会急剧增加，导致索引检索性能下降。尤其是在Series Segment Index中，检索性能的下降更为明显
  - TSI（Time Series Index）检索Measurement，tag，tagval，time
  - TSM（Time-Structured Merge Tree）用来检索time-series -> value
  - Series Segment Index 用来检索 time-series key <–> time-series Id, Series ID 在 InfluxDB 中是一个唯一的标识符，用于识别和索引单个时间序列数据。
- 内存压力增加：在进行compaction操作时，系统需要在内存中加载所有的series key来构建新的hash table，并将其mmap存储到磁盘。当series key数量过多时，可能会导致内存不足，甚至出现OOM（Out of Memory）问题
- 磁盘I/O增加：由于高基数问题导致的索引膨胀，会增加对Series Segment文件的I/O访问，特别是在compaction过程中，这可能会导致大量的磁盘I/O操作，影响数据库的整体性能
- 数据文件膨胀：在TSM存储引擎中，已经删除的数据点会被标记为tombstone，但不会立即从磁盘上物理删除。随着时间的推移，这些被标记为删除的数据会导致SeriesSegment文件持续膨胀，增加了存储空间的消耗


解决方式:
- 正排索引是 database 级别的，增加partition或者database, 减少 compaction 时的内存
  - 新数据
- 修改时间线存储策略
  - 当 partition 大于某个阈值时， hash 索引 ->  b+tree 索引
- 将series key的正排索引下沉到shard级别
- 根据Measurement修改时间线存储策略
  - 对做 series key 的正排索引的 compaction 时，可以添加 Measurement 时间线统计，如果某个 Measurement 的时间线膨胀时，可以将这个 Measurement 的所有 series key 切换到 B+ tree。


### REF
- [时序数据库永远的难关 — 时间线膨胀(高基数 Cardinality)问题的解决方案](https://developer.aliyun.com/article/786289)



## REF
- [docs](https://docs.influxdata.com/)
    - [schema-design](https://docs.influxdata.com/influxdb/clustered/write-data/best-practices/schema-design/)
- [influxdata/influxdb](https://github.com/influxdata/influxdb) 3.x rust版本 
  - main-2.x  2.0 版本
- [Time Series Index (TSI) details](https://docs.influxdata.com/influxdb/v1/concepts/tsi-details/)
- [InfluxDB的存储引擎演化过程](https://developer.aliyun.com/article/727640)
  


- [influxdb storage_engine TSM](https://jasper-zhang1.gitbooks.io/influxdb/content/Concepts/storage_engine.html) 中文
  - 时间序列数据的属性
  - TSM的产生

- [InfluxDB 模型和存储引擎入门](http://47.241.45.216/2022/03/17/InfluxDB-%E7%9B%B8%E5%85%B3%E6%9D%90%E6%96%99/)

- [解读 InfluxDB IOx：基于列存的时序数据库](https://liujiacai.net/blog/2021/01/21/thoughts-of-influxdb-iox/)
  - 对于时间线膨胀问题，IOx 不再单独维护倒排索引，取而代之的是每个分区的概要文件。在分区选择合理的情况下，概要文件的大小是比较可控的。相当于对之前的倒排索引做了分片。

- [开源时序数据库解析 - InfluxDB IOx](https://zhuanlan.zhihu.com/p/534035337)
  - 问题：
    - 1）当时间线基数变大，索引大小会膨胀，会导致查询性能的急剧下降；
    - 2）某些场景下索引大小会远大于数据大小（例如 Trace 场景，单条时间线包含极少数据点，时间线基数非常大），导致存储效率大大降低；
    - 3）某些时间线规模较大且较低索引筛选率的查询场景，索引几乎无效甚至会导致查询性能的严重下降。
  - 解决问题的方式就是干脆把整个时间线索引给去除
  - PS：与 Rockset 实现路径很相近


## ES 原理


### Mapping

Elasticsearch Mapping 是对索引中文档字段的数据类型、存储方式、分析设置等关键属性的定义，类似于关系型数据库中的表结构定义。是ES实现动态schema的背后技术。

1. 基本概念
Mapping 定义了文档的结构，包括字段名、字段类型、是否被索引、分析器选择等。
动态 Mapping 当向索引中插入文档时，如果文档中的字段没有在Mapping中预先定义，Elasticsearch可以根据字段的值自动推断其类型并创建相应的Mapping。但动态Mapping可能导致类型冲突，因此在生产环境中建议明确指定Mapping。
2. 字段类型
Text & Keyword：text 类型适用于全文本搜索，经过分析器处理生成倒排索引；keyword 类型不做分析，适合精确值匹配，如ID、标签。
Numeric：支持多种数值类型，如long、double，优化存储和范围查询。
Date：存储日期/时间，支持多种格式，并可配置时区。
Object & Nested：object 用于嵌套的对象，保持父子关系；nested 类型则允许对象数组中的每个对象独立查询。
3. 分析器
分析器负责将文本字段转换成词项（tokens）以便索引和搜索。它包括字符过滤器、分词器和token过滤器三个阶段。
可以为不同的字段指定不同的分析器，以满足特定的搜索需求。
4. 索引设置
是否索引：控制字段是否参与全文搜索，未被索引的字段不能被搜索到。
norms：影响文档评分，可用于节省存储空间和加快查询速度。
doc_values：优化聚合和排序操作，占用较少的内存。
5. Mapping 参数
enabled：控制字段是否被索引。
store：决定字段值是否以原始形式存储，以便检索时直接获取。
coerces：是否允许Elasticsearch自动转换字段类型。
ignore_above：对于text字段，超过指定长度的值将被忽略，避免大值导致的问题。
6. 动态Template
动态模板允许用户为未知字段定义默认的Mapping设置，这样在动态Mapping过程中，新字段可以根据预设的规则自动应用特定的类型和设置。
7. 更新Mapping
虽然Mapping可以更新，但某些更改（如改变已存在字段的数据类型）可能需要重新索引数据。
使用PUT _mapping API可以更新索引的Mapping。
8. 查看Mapping
可以通过GET /index_name/_mapping API来查看索引的当前Mapping。
Elasticsearch的Mapping设计对索引的性能、查询效率及存储空间有着直接影响，因此合理设计Mapping是至关重要的。




### 一致性协议

PacificA类算法  < 7.x

raft 


### TSDB

ES做时序引擎：

- [Add better support for metric data types (TSDB)](https://github.com/elastic/elasticsearch/issues/74660)
- [TSDB dimensions encoding](https://github.com/elastic/elasticsearch/pull/99747)
    - 
- [TSDB numeric compression](https://github.com/elastic/elasticsearch/pull/92045)

- [基于Elasticsearch的指标可观测实践](https://zhuanlan.zhihu.com/p/562493025)
    - Setting中增加了一个index.mode=time_series的设置，这个设置告诉ES在内部去实现时序场景的最佳实践。
    - Mapping 字段配置增加了2个关键字：time_series_dimension和time_series_metric，这两个设置是为了告诉ES哪些字段用作维度字段，哪些字段用作指标字段，有这两个配置再结合index.mode=time_series，ES会把所有的维度字段生成一个_tsid（时间线ID）内部字段，用_tsid和timestamp去做 index sorting。


实现

- ES87TSDBDocValuesConsumer
- ES87TSDBDocValuesProducer

#### 编码

- timestamp：delta coding + GCD compression + bit-packing



## REF

-  [es blog cn](https://www.elastic.co/cn/blog/)

- [Elasticsearch分布式一致性原理剖析(一)-节点篇](https://developer.aliyun.com/article/797309)
- [Elasticsearch-05-数据一致性](https://www.cnblogs.com/primabrucexu/p/15009955.html)
    - PacificA类算法
- [Elasticsearch 集群协调迎来新时代](https://www.elastic.co/cn/blog/a-new-era-for-cluster-coordination-in-elasticsearch) official
- [ElasticSearch 7.x的raft算法选主流程](https://cloud.tencent.com/developer/article/1826426)

- [如何让ES低成本、高性能？滴滴落地ZSTD压缩算法的实践分享](https://armsword.com/2023/08/11/didi-es-zstd/)
    - 对行存文件更改ZSTD压缩算法，集群CPU使用率下降15%，写入性能提升25%。平均索引存储下降达到30%。
- [](https://github.com/tencentyun/qcloud-documents/blob/master/product/%E5%A4%A7%E6%95%B0%E6%8D%AE%E4%B8%8EAI/Elasticsearch%20Service/ES%E5%86%85%E6%A0%B8%E5%A2%9E%E5%BC%BA/%E5%8E%8B%E7%BC%A9%E7%AE%97%E6%B3%95%E4%BC%98%E5%8C%96.md)

- [自实现zstd](https://github.com/LuXugang/Lucene-7.x-9.x/issues/40)

- [opensearch zstd](https://github.com/opensearch-project/OpenSearch/pull/3577) + [zstd memory leak fix](https://github.com/opensearch-project/OpenSearch/pull/9403)
    - [experimental zstd benchmarks](https://github.com/opensearch-project/OpenSearch/issues/7805)

- [京东ES支持ZSTD压缩算法上线了:高性能，低成本](https://www.cnblogs.com/Jcloud/p/17964961)


- [【离线】esrally实践总结](https://developer.aliyun.com/article/851848) 基准测试

- [业界使用 ES 的一些工程实践](https://www.cnblogs.com/hapjin/p/17892378.html)

- mapping
    - [一文搞懂 Elasticsearch 之 Mapping](https://www.cnblogs.com/wupeixuan/p/12514843.html)  数据类型
    - [Elasticsearch中mapping全解实战](https://www.cnblogs.com/youngdeng/p/12867728.html)


## 倒排索引 Inverted index

倒排索引（Inverted Index）是一种数据结构，广泛应用于信息检索领域，特别是在搜索引擎中。它的设计目的是为了快速查找包含特定单词或术语的文档。与传统索引（正排索引）按照文档来组织单词不同，倒排索引是按照单词来组织文档，因此得名“倒排”。

## REF

- [Lucene](https://github.com/apache/lucene)  java

- [Apache Doris](https://github.com/apache/doris)  基于[CLucene](https://github.com/apache/doris-thirdparty/blob/d3de160/src/core/CLucene.h) 非常老的项目
    - https://www.infoq.cn/article/kmui4okixhx4mvpqh3cd  
    

- [clickhouse](https://github.com/ClickHouse/ClickHouse) [inverted index](https://github.com/ClickHouse/ClickHouse/blob/master/docs/en/engines/table-engines/mergetree-family/invertedindexes.md)

- [alibaba/havenask](https://github.com/alibaba/havenask) 自己实现
    - [倒排索引介绍](https://github.com/alibaba/havenask/wiki/%E5%80%92%E6%8E%92%E7%B4%A2%E5%BC%95%E4%BB%8B%E7%BB%8D)
    - [倒排索引类型](https://github.com/alibaba/havenask/wiki/%E5%80%92%E6%8E%92%E7%B4%A2%E5%BC%95%E7%B1%BB%E5%9E%8B)


- [infinity](https://github.com/infiniflow/infinity) c++
    - [倒排](https://github.com/infiniflow/infinity/blob/main/src/storage/invertedindex/)、向量，自己实现的简易版本，认为Lucene的历史负担，打分等搜索需求历史负担，可以简化
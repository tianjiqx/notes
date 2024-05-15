
## ES 原理


### 一致性协议

PacificA类算法  < 7.x

raft 

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
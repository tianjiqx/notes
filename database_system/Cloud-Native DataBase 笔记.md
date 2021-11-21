# Cloud-Native DataBase 笔记

## 1.背景

- 云资源能力，效率
  - [S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)等兴盛
  - 新硬件GPU，RDMA，NVMe
- 部署方式
  - 存算分离
    - 价格
    - 存储的容错保证
      - 纠删码?
    - 独立扩展性



## 2. 主题

### 2.1 计算pushdown

pushdownDB

S3 支持带计算的查询，性能根据效率过滤提升，但是存在额外的计算花费。需要tradeoff。

最终pushdownDB，使用传统计算下推优化在S3存储使用上，计算时间提升6.7x，花费减少30%



开放性问题：

- 数据库的功能切分，哪些放到存储端？
  - REDO（Aurora，SQL Server）

### 2.2 Cache

FlexPushdownDB 基于pushdownDB，增加缓存系统，cache数据到本地计算结算节点。

- 列存，segement粒度，缓存原始表数据。
- 缓存优先，pushdown次之，否则S3
  - 缓存淘汰策略，不能pushdown的数据权重更高，更应该缓存

cache size -> 无限大，即变成share nothing的节点。

FlexPushdownDB 在pushdown基础上提升2.2倍（缓存12GB）

## 3.系统

### 3.1 PolarDB



### 3.2 GaussDB/OpenGaussDB



## 3.3 Snowflake



## REF

- [bilibili: Xiangyao Yu：Optimizing Cloud-Native Databases with Storage Disaggregation](https://www.bilibili.com/video/BV1J34y1D7Zi?from=search&seid=2020848151569080804&spm_id_from=333.337.0.0)
  - [Xiangyao Yu](http://pages.cs.wisc.edu/~yxy/) wisc 助理教授
- [Choosing A Cloud DBMS: Architectures and Tradeoffs](https://pdfs.semanticscholar.org/3ccf/fee80e25b44b9c48f91a110239f4abfa0c29.pdf) cloud DBMS evalution 
  - 实验结论
    - S3 storage bandwith ~500MB
    - local SSD  bandwith > 14GB/s (shared-nothing  10x faster)
- [PushdownDB: Accelerating a DBMS using S3 Computation](http://pages.cs.wisc.edu/~yxy/pubs/pushdowndb-icde.pdf)
- [FlexPushdownDB: Hybrid Pushdown and Caching in a Cloud DBMS](http://pages.cs.wisc.edu/~yxy/pubs/fpdb.pdf)
- [PolarDB-X](https://github.com/ApsaraDB/galaxysql)  ApsaraDB/galaxysql
- [OpenGaussDB](https://gitee.com/opengauss)






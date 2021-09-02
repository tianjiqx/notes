# Snowflake-笔记

## 1. 云环境特点

### 1.1 AWS S3

Amazon Simple Storage Service (Amazon S3) 是一种对象存储服务，可提供业界领先的可扩展性、数据可用性、安全性和性能。

典型应用：湖内数仓、网站、移动应用程序、备份和还原、存档、企业级应用程序、IoT 设备和大数据分析的数据存储



特性：

- 易于使用
  - 有基于 Web 的管理控制台和移动应用程序
  - 提供REST API 和软件开发工具包，与第三方集成
- 高持久性
  - 99.999999999％ (11 个 9)
- 可扩展
- 安全性
  - 数据上传加密,SSL/TLS
  - Amazon Identity and Access Management (IAM) 管理对象权限并控制对数据的访问
- 高可用
  - 年度99.99% 可用 协议
- 低成本
  - 存储：每 GB ¥ 0.1755 / 月  （50TB内，使用更多，价格降低）
    - 分层管理服务，自动冷热数据优化
  - 请求：
    - PUT、COPY、POST 或 LIST 请求：每 1000 个请求 ¥ 0.00405
    - GET、SELECT 及所有其他请求：每 10000 个请求 ¥ 0.0135
      - 扫描数据：每 GB ¥ 0.01433
      - 返回的数据：每 GB ¥ 0.0051
  - 数据传输：
    - 传出到互联网，每 GB ¥ 0.933（促销）
  - （计费很复杂，但是在短期使用上相对于自购服务器应该会是比较便宜的价格）
- 集成其他服务
  - 如Redshift



性能：

- 每秒至少支持 3500 个添加数据请求
- 每秒至少支持 5500 个检索数据请求
- 较小的请求（例如，小于 512 KB）时，中间延迟通常在几十毫秒范围内
- 高吞吐
  - 8-16 MB 粒度的并发请求，85–90 MB/s
  - 大约 15 个并发请求，打满25 Gb/s 或 100 Gb/s NIC



缺点：

（TODO）

延迟和并发？



（单纯只被动适应云服务提供商提供的服务，或者说简单的直接使用器服务，来设计系统，或者取代部分模块（存储）可能是不够的，可能还是需要向云服务提供商提供需求，或者可能需要再组织一套系统，为上层系统提高数据等内容）











## REF

- [doc](https://docs.snowflake.com/en/)
- [Snowflake 架构讨论 《The Snowflake Elastic Data Warehouse》](http://ilongda.com/2020/01/05/snowflake/)
- [paper: The Snowflake Elastic Data Warehouse](http://pages.cs.wisc.edu/~yxy/cs839-s20/papers/snowflake.pdf)
- [slides: The Snowflake Elastic Data Warehouse SIGMOD 2016 and beyond](https://15721.courses.cs.cmu.edu/spring2018/slides/25-snowflake.pdf)
- [云原生OLAP数据引擎](https://zhuanlan.zhihu.com/p/200955929)
- [存算分离/DB on K8s 论文/blog收集](https://zhuanlan.zhihu.com/p/377755864) 
- [美团内部讲座｜周烜：华东师范大学的数据库系统研究](https://zhuanlan.zhihu.com/p/275870856) 分布式事务，拆分，基于新硬件的， 高速缓存系统
- [Amazon S3 功能](https://aws.amazon.com/cn/s3/features/)
- [Amazon S3](https://www.amazonaws.cn/s3/?nc2=h_ql_prod_st_s3) 功能，定价
- [一文读懂 AWS S3](https://zhuanlan.zhihu.com/p/112057573)
- [Amazon S3 的性能设计模式](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html)


# DataFuse 笔记

[TOC]

## 1. 简介

Datafuse 是一个开源的**弹性**和**可扩展的**云数据仓库Cloud Warehouse，使用存储在云存储系统（例如 AWS S3 和 Azure Blob Storage 或其他）中的数据执行工作负载。

面向云环境的OLAP系统。最开始根据TensorBase作者的评价，以为对标的是rust的Clickhouse，但是根据最近Datafuse博客，它其实对标Snowflake，AWS Redshift。



特点：

- Rust语言编写
- 弹性，可扩展
  - 存储和计算资源可以按需动态扩展和缩减
  - 按资源付费
- 保护
  - 云环境，所有数据文件和网络流量都经过端到端加密
  - SQL级别基于角色的访问控制
    - K8S RBAC（Role-based access control）
- 支持MySQL，clickhouse 客户端



（PS：注意目前0.4.x版本， 一些特点可能还只是期望，或者实现中，无法用于生产）



Datafuse 对传统数仓架构的批评：

- Sharding Warehouse

  - 类似share nothing架构的，没有将计算和存储分离，不适合云环境（资源粒度控制）
    - (根据OB 的tpch测试报告，其也算是计算与存储分离，有专门的OFS文件系统作为其存储支持，ObServer节点只保留少量的的SSD)
  - 容易发生数据热点问题
  - 扩容，数据均衡，需要花费时间进行副本迁移

- Presto/spark + Shared Storage(AWS S3，Blob Storage)

  - 共享存储服务存在延迟、抖动问题
    - （OLTP型数据库要更重视这个问题，OLAP其实应该并不太需要在意才是）

  



  **设计理念**：

  Cloud Warehouse里的状态：

  - Persistent data
    - 用户数据，存储在Shared Storage
  - Intermediate data
    - 排序、join shuffle中间结果文件
  - Metadata
    - object catalogs, table schema, user 等元数据

  

  设计：

- 通过cache Shared Storage上的数据到计算层节点，避免网络抖动。

  - 失效，从S3查询，新增Latency抖动。
  - Snowflake 在计算和存储之间加了一个共享的Distributed Ephemeral Storage 存储Intermediate data
    - 资源隔离问题 （TODO：Distributed Ephemeral Storage简单搜索暂未找到说明，只VM 计算节点有cache模块，作者取名的吗）
    - Snowflake 使用的优势似乎是提供了强大的数据管理服务，开箱即用的数据湖，数据仓库
- Datafuse状态分离
  - 为Persistent data生成足够多的索引放到Metadata Service，计算节点进行订阅，更新本地cache
    - 海量索引块的同步
    - Persistent data 怎么处理？

![](datafuse笔记图片/v2-56d66f4cf2971f9c111342ac4d444d64_720w.jpg)





## 2. 架构与设计

![](datafuse笔记图片/datafuse-arch-20210817.svg)

架构与Snowflake 架构图确实非常相似。

- Meta Services
  - 多租户、高可用的分布式 key-value 存储服务，支持事务
  - `Metadata` : 表的元信息、索引信息、集群信息、事务信息等
  - `Administration`：用户系统、用户权限等
  - `Security` ：用户登录认证、数据加密等
- Computing Services
  - 由多个集群（cluster）组成，不同集群可以承担不同的工作负载
    - 集群由多个节点组成
  - 执行计划 生成（Planner）
    - 处理SQL
  - 优化器（Optimizer）
    - 当前只有基于规则的优化
  - 处理器（processors）
    - 根据执行计划，处理器们被编排成一个流水线（Pipeline），用于执行计算任务
      - 是MR，不是MPP？
        - 分布式计划，使用了arrow-flight，应该会将shffle数据落盘
  - 缓存（cache）
    - 使用本地 SSD 缓存热点数据和索引
      - LOAD_ON_DEMAND - 按需加载索引或数据块（默认）。
      - LOAD_INDEX - 只加载索引。
      - LOAD_ALL - 加载全部的数据和索引，对于较小的表可以采取这种模式。
- Shared Storage
  - 存储格式
    - Parquet 数据文件，按主键排序
    - min_max.idx （整个文件的min max）, sparse.idx 索引文件
      - 学习clickhouse的存储设计
  - 文件系统（IFileSystem）抽象存储层
    - Local FS
      - 使用本地磁盘文件夹作为存储，单节点
    - DFS
      - aws-S3 的存储服务
    - Object Storage Adapters
      - 基于云上对象存储服务
  - 分布式文件系统 DFS
    - 元数据集群
      - 数据的位置信息
      - 每个节点都持有一份元信息的副本
        - raft组，大部分节点只是学习者，不参与选主
          - 学习tidb TiFlash？
    - 块存储集群
      - 提供读取，写入API





## 3. 实现







## REF

- [github:datafuse](https://github.com/datafuselabs/datafuse.git)
- [doc:datafuse](https://datafuse.rs/overview/architecture/)
- [Rust, Datafuse and the Cloud Warehouse（1）云时代数仓架构设计](https://zhuanlan.zhihu.com/p/402092313) 设计理念
- [Rust, Datafuse and the Cloud Warehouse（2）Datafuse 架构概览](https://zhuanlan.zhihu.com/p/402093492)
- [Best Software to Build a Data Warehouse in the Cloud: Features, Benefits, Costs](https://www.scnsoft.com/analytics/data-warehouse/cloud)
- [未来数据库应具备什么核心能力？](https://pingcap.com/zh/blog/core-competence-of-future-database)
- [云原生数据库设计新思路](https://pingcap.com/zh/blog/new-ideas-for-designing-cloud-native-database)
- [[Snowflake核心技术解读系列一]架构设计](https://developer.aliyun.com/article/780125)


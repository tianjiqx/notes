# 论文笔记 - Impala: A Modern, Open-Source SQL Engine for Hadoop

## 0.阅读动机

- 看到一篇关于impala介绍过其批处理和MPP融合的文章，对其细节感兴趣（不过论文是2015年的，估计没有相关内容，但是了解原始设计理念吧）
- SQL on Hadoop的一个典型，观察如何做查询执行，以及一些设计考虑
- 试验（Jiri Srba）[论文阅读步骤](https://github.com/tianjiqx/notes/blob/master/%E7%A8%8B%E5%BA%8F%E5%91%98%E7%9A%84%E8%87%AA%E6%88%91%E4%BF%AE%E5%85%BB/%E6%80%8E%E6%A0%B7%E8%AF%BB%E6%96%87%E7%8C%AE%E5%92%8C%E5%81%9A%E9%99%88%E8%BF%B0-%E7%AC%94%E8%AE%B0.md)



## 1. 概览

（摘要，引言，结论）

### 1.1 论文针对的问题

解决**Hadoop** 上的 BI/分析（主要是查询），提供**低延迟**和**高并发性**。（支持多用户）



### 1.2 论文作者的认为的贡献、优势

贡献：

- 为Hadoop环境，构建了一个开源的、完全的，先进的MPP SQL查询引擎。
  - 非批处理hive、spark的系统
  - 引入并行DBMS技术（MPP，运行时代码生成）

优势：

- 性能与商业OLAP一样或者更好，同时保留灵活性和Hadoop的成本
- 良好的开放模块化架构，混合文件格式、处理框架，能够更广泛的支持其他业务
  - 多样的存储支持
  - 可以与其他处理引擎协作（spark，hive，hbase）



### 1.3 现实意义

更高性能、并发的SQL on Hadoop，并且是开源产品可以实际尝试，部署应用，并且到现在（2021）依然在维护。



## 2. 整体了解

（基础Preliminaries，主体Body）

（问题定义，相关工作，系统设计，实验）

### 2.1 Impala与传统RDBMS的区别（用户角度）

商业环境集成，支持行业标准：

- 客户端可以通过 ODBC 或 JDBC 连接
- 使用 Kerberos 或 LDAP 完成身份验证
- 授权遵循标准的 SQL 角色和权限
- 标准SQL查询语法
  - 建表时特殊有额外语句

区别：

#### 2.1.1 物理schema设计

建表时，用户可以指定存储路径，分区列，存储格式。（与hive类似）

- 无分区，根目录
- 有分区，增加分区目录。（HDFS的路径）
  - 特别的可以修改分区格式，原始text，后期批处理为parquet

存储格式：

- 压缩、非压缩的文本文件
- RCFile（列存格式）
- Avro（二进制格式）
- Parquet（性能最好，列存格式）

#### 2.1.2 SQL支持

由于 HDFS 作为存储管理器的限制。

不支持传统UPDATE 或 DELETE行，只能批量插入（INSERT INTO ... SELECT ...）。

按分区删除。



后来支持Kudu的UPDATE 或 DELETE。



### 2.2 架构设计

![](impala笔记图片/impala.png)

impala自身是一个大规模并行查询执行引擎，无存储引擎，依赖于HDFS、HBASE。

与一般的MPP不同，计算与存储是分离的。

-  Impalad守护进程（对称架构）
  - 接受来自客户端进程的查询并协调它们在整个集群中的执行，以及处理其他 Impala守护进程执行单个查询片段
  - 每个节点部署一个Impalad，同时节点上也有一个HDFS的DataNode
  - 组件
    - Query Planner
    - Query Coordinator
    - Query Executor
- Statestore守护进程
  -  Impala 的元数据发布订阅服务，它将集群范围的元数据传播到所有 Impala 进程
- catalogd目录守护进程
  - Impala 的目录存储库和元数据访问网关
  - 反应Hive Metastore的变更，对catalogd的更改，通过 statestore 广播



要解决的核心问题：

- 状态分发
  - 集群范围元数据的协调和同步
  - 对称节点都能够接受和执行查询
    - 需要具有最新版本的系统catalog和 Impala集群成员的最新视图，以安排查询
  - 解决方案：发布订阅系统statestore
- 统一、全局的的元信息管理
  - Catalog服务，提取第三方元数据存储信息，聚合到Impala的Catalog中



架构分层

- 前端
  - 负责将 SQL 文本编译为 Impala 后端可执行的查询计划
  - Java
  - 组件
    - SQL 解析器
    - 基于成本的查询优化器
    - 两阶段优化
      - 解析树翻译为不可执行的单节点计划树
      - 单节点计划，生成分布式执行计划
        - 总体目标是**最小化数据移动**并**最大化扫描局部性**
- 后端
  - 从前端接收查询片段并负责它们的快速执行
  - C++
  - 运行时代码生成
  - Volcano执行模型+Exchange算子
    - 每个next是一批记录
    - 尽量pipeline，最大限度地减少存储中间结果的内存消耗
  - 可溢出的算子（刷磁盘）
    - 散列连接
    - （基于散列的）聚合
    - 排序
    - 分析函数的eval
  - 高效的IO管理器
    - 近磁盘带宽的读取
    - 吞吐量比其他测试系统高 4 到 8 倍

- 资源负载管理
  - 用以支持每秒数千个查询的工作负载
    - 直接使用原生的yarn服务，集中决策无法满足需求，资源请求和响应周期过长
  - 独立的准入控制机制，进行低延迟决策
    - 避免集中决策
  - Llama服务
    - 资源缓存
    - 未命中再向yarn申请



### 2.3 实验

#### 2.3.1 单用户查询响应

![](impala笔记图片/Snipaste_2021-08-23_23-15-01.png)

以零思考时间重复提交查询测试。

 Impala 的性能优势从 2.1 倍到 13.0 倍不等，平均快 6.7 倍。

#### 2.3.2  多用户查询响应

![](impala笔记图片/Snipaste_2021-08-23_23-22-02.png)

 10 个并发用户，Impala 的性能比其他系统高 6.7 倍到 18.7 倍，吞吐量比其他系统高 8.7 倍到 22 倍。。

#### 2.3.3 与商业关系数据库比较

![](impala笔记图片/Snipaste_2021-08-23_23-22-15.png)

30TB的TPC-DS，平均性能高出 2 倍（这里的比较是每个测试case的性能倍数取平均，非测试集总时间倍数），只有三个查询的执行速度更慢。



## 3. 精读

（主体的每一处细节，参考文献）

### 3.1 元信息管理



### 3.2 执行计划生成



### 3.3 运行时代码生成



### 3.4 IO管理器



### 3.5 资源管理



### 3.6 参考文献

A. Floratou, U. F. Minhas, and F. Ozcan. SQL-on- Hadoop: Full circle back to shared-nothing database architectures. PVLDB, 2014. 本文多处引用此文的一些测试结论。

C. Lattner and V. Adve. LLVM: A compilation frame- work for lifelong program analysis & transformation. In CGO, 2004. 代码生成技术LLVM

T. Willhalm, N. Popovici, Y. Boshmaf, H. Plattner, A. Zeier, and J. Schaffner. SIMD-scan: ultra fast in- memory table scan using on-chip vector processing units. PVLDB, 2, 2009. 代码生成 SIMD



V. K. Vavilapalli, A. C. Murthy, C. Douglas, S. Agarwal, M. Konar, R. Evans, T. Graves, J. Lowe, H. Shah, S. Seth, B. Saha, C. Curino, O. O’Malley, S. Radia, B. Reed, and E. Baldeschwieler. Apache Hadoop YARN: Yet another resource negotiator. In SOCC, 2013. yarn的资源调度



## 4. 个人总结



评分：7.3/10



（试验体会：文献阅读的技巧，只是阅读，但是最后的笔记结果，组织起来还是需要重新组织、调整把精读的内容填充进文章整体了解，不能会划分太散，以及不够清晰，并且有时会插入一些最新的内容，其他相关比较内容。

第2,3节应该合并在一起。

另外，文献阅读技巧，简单讲，就是从浅到深，由易到难，摘要，结论很简单，可以先看，了解框架，论文结构，相关名词，实验结果，也相对容易，最后是深入细节，原理实现，参考文献，在整个过程中，逐渐判断论文价值，符不符合自己的看这篇论文的动机、兴趣，及时止损。）



## REF

- Kornacker, M., Behm, A., Bittorf, V., Bobrovytsky, T., Ching, C., Choi, A., … Yoder, M. (2015). Impala: A modern, open-source SQL engine for Hadoop. CIDR 2015 - 7th Biennial Conference on Innovative Data Systems Research.
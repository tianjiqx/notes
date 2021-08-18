# 列存储(Column-Oriented)数据库系统

[TOC]

## 1. 简介

列存储Column-Oriented，即数据记录按列方式组织column by column，相对于行存储使用tuple by tuple。



列存储出现的背景：

列存出现的直接原因，是数据库系统性能与系统在主存储器（例如磁盘）上存储数据并将其移入 CPU 寄存器进行处理的效率直接相关。即IO是数据库系统的瓶颈。



IO改进的其他探索：

- 复杂的索引
- 物化视图
- 垂直和水平分区



列存储的场景：

采用列存储的数据库，通常是一些OLAP负载的数据库，因为列存格式，能够快速扫描、聚合需要的列，倾向于不更新数据。



典型列存储系统：

学术：MonetDB，、VectorWise、C-Store

商业：VectorWise，Vertica



并且许多大数据系统也使用列存储格式：

ClickHouse，Druid，Greenplum，Amazon  Redshift。



一些系统或多或少借鉴列存储的思想：

HBase，Impala，TiDB



## 2. 数据模型



### 2.1 Apache ORC





### 2.2 Dremel / Apache Parquet



主内存列存储 Apache Arrow

磁盘驻留列存储Apache  Parquet/ORC



区别：

Parquet 和 ORC，支持高比率压缩算法（snappy，zlib，lz4）

Arrow 专注于矢量化处理和和低开销压缩算法（字典压缩等），批量大小可以更小



## 3. 编码与压缩





## 4. 索引





## 5. Join





## REF

- [The Design and Implementation of Modern Column-store Database Systems](https://stratos.seas.harvard.edu/files/stratos/files/columnstoresfntdbs.pdf)
- [处理海量数据：列式存储综述（存储篇）](https://zhuanlan.zhihu.com/p/35622907)
- [[笔记] Integrating Compression and Execution in Column-Oriented Database Systems](https://fuzhe1989.github.io/2021/01/08/integrating-compression-and-execution-in-column-oriented-database-systems/)
- [slides:压缩和列存储](https://info290.github.io/slides/19-compression-col-stores.pdf)
- [slides:Column_Store_Tutorial_VLDB09](http://www.cs.umd.edu/~abadi/talks/Column_Store_Tutorial_VLDB09.pdf)
- [slides:column-store-tutorial](https://github.com/tianjiqx/slides/blob/master/column-store-tutorial.pdf)
- [slides:Revisiting Data Compression in Column-Stores-2021](https://cs.ttu.ee/events/medi2021/slides/Slesarev_MEDI2021.pdf)
- [slides:Column-Stores vs. Row-Stores: How Different are they Really?](https://www.slideshare.net/abadid/columnstores-vs-rowstores-how-different-are-they-really)
- [Apache Arrow 与 Parquet 和 ORC：我们真的需要第三个 Apache 项目来表示列数据吗？](http://dbmsmusings.blogspot.com/2017/10/apache-arrow-vs-parquet-and-orc-do-we.html)
- [slides:ORC Deep dive 2020](https://www.slideshare.net/oom65/orc-deep-dive-2020)
- [slides:File Format Benchmarks - Avro, JSON, ORC, & Parquet-2016](https://www.slideshare.net/oom65/file-format-benchmarks-avro-json-orc-parquet)


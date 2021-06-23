# HBase笔记

[TOC]

## 1. 场景、架构和优缺点

见[大数据系统鉴赏](https://github.com/tianjiqx/notes/blob/master/big_data_system/%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%B3%BB%E7%BB%9F-%E9%89%B4%E8%B5%8F.md) hbase小节



## 2.数据模型

#### 2.1 逻辑视图

使用角度——表、行、列。

- table：表，一个表包含多行数据。

- row：行，一行数据包含一个唯一标识rowkey、多个column以及对应的值。表中按照rowkey的字典序由小到大排序。
- column：列，columnfamily（列簇）以及qualifier（列名）两部分组成，两者中间使用":"相连。
  - column family在表创建的时候需要指定，用户不能随意增减
  - qualifier可以动态增加
- timestamp：时间戳，每个cell在写入HBase的时候都会默认分配一个时间戳作为该cell的版本，用户也可指定
- cell：单元格，由五元组（row, column, timestamp, type, value）组成的结构，其中type表示Put/Delete这样的操作类型，timestamp代表这个cell的版本。这个结构在数据库中实际是以KV结构存储的，其中（row, column,timestamp, type）是K，value字段对应KV结构的V。

![](hbase笔记图片/Snipaste_2021-06-24_01-29-58.png)

![](hbase笔记图片/Snipaste_2021-06-24_01-43-34.png)

cell的KV存储结构：

![](hbase笔记图片/Snipaste_2021-06-24_01-33-45.png)

多维稀疏排序Map

- 多维: key是复合结构
- 稀疏：null值不存，所以列理论上可以无限扩张
- 排序：KV在一个文件中，按key排序，不仅rowkey，其他组成也参与。



#### 2.2 物理视图

HBase中的数据是**按照列簇存储**的，即将数据按照列簇分别存储在**不同的目录**中。

![](hbase笔记图片/Snipaste_2021-06-24_01-44-23.png)

注意，anchor列族有两列

列族存储：结语行存和列存之间，可以随意在行存（多列名），列存（1列族1列名）之间转换



列存优势：读取IO减少，压缩率高。

更多列存细节内容，见个人slide:[column-store-tutorial](https://github.com/tianjiqx/slides/blob/master/column-store-tutorial.pdf)



## 3.Client与服务端的交互

#### 3.1 hbase:meta 表



## ４.HBase读写流程



## 5. Compaction



## 6. Region负载均衡(迁移，合并，分裂)





## Q&A

### 1. HBase只支持单行事务，稀疏存储，是不是完全设计成大宽表就好？

HBase对列族没有限制，但是，按行进行切分region的，memstore,HFile大小有限（需要保障读取性能，不能完全一个大文件），列多意味着需要切分的region多。如果region数量过多，hmaster 内存无关管理，并且影响性能，所以不是越宽越好。（在星环时，甚至只推荐一个列族）

Region数量与大小的最佳实践

> 官方指出每个RegionServer大约100个regions的时候效果最好.
>
> - [HBase](https://cloud.tencent.com/product/hbase?from=10680)的一个特性MSLAB，它有助于防止堆内存的碎片化，减轻垃圾回收Full GC的问题，默认是开启的。但是每个MemStore需要2MB（一个列簇对应一个写缓存memstore）。所以如果每个region有2个family列簇，总有1000个region，就算不存储数据也要3.95G内存空间。
> - 如果很多region，它们中Memstore也过多，内存大小触发Region Server级别限制导致flush，就会对用户请求产生较大的影响，可能阻塞该Region Server上的更新操作。
> - HMaster要花大量的时间来分配和移动Region，且过多Region会增加ZooKeeper的负担。
> - 从HBase读入数据进行处理的mapreduce程序，过多Region会产生太多Map任务数量，默认情况下由涉及的region数量决定。



## REF

- [HBase原理与实践-胡争](https://weread.qq.com/web/reader/632326807192b335632d09ckc81322c012c81e728d9d180) 微信读书网页版，微信刷码即可，**推荐分析原理解析时阅读**
- 《HBase实战》
- [HBase官方中文文档](http://hbase.org.cn/)
- [Hbase最佳实战：Region数量与大小的重要影响](https://zhuanlan.zhihu.com/p/27800787)


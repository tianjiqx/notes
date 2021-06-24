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

### 



### 4.1 hbase写



### 4.2 hbase flush

Flush：Memstore刷HFile到hdfs上的过程。

触发方式：

- 手动
  - shell命令 flush ‘tablename’或者flush ‘region name’分别对一个表或者一个Region进行flush。
- 超过阈值
  - Memstore级别限制：当Region中任意一个MemStore的大小达到了上限（hbase.hregion.memstore.flush.size，默认128MB），会触发Memstore刷新。
  - Region级别限制：当Region中所有Memstore的大小总和达到了上限（hbase.hregion.memstore.block.multiplier * hbase.hregion.memstore.flush.size，默认 2* 128M = 256M），会触发memstore刷新。
  - Region Server级别限制：当一个Region Server中所有Memstore的大小总和达到了上限（hbase.regionserver.global.memstore.upperLimit ＊ hbase_heapsize，默认 40%的JVM内存使用量），会触发部分Memstore刷新。
- HBase定期刷新Memstore：默认周期为1小时

**MemStore的最小flush单元是HRegion而不是单个MemStore。**Region->Stores（memstore+HFiles），Store对应一个列族。为什么不能单独刷新，因为可能涉及region 切分，所有列族必须统一。减少列族数量，可以减少每次flush的IO开销



#### REF

- [HBase Flush 解析](https://blog.csdn.net/u010039929/article/details/74253093)



### 4.3 hbase读



## 5. Compaction

Compaction是从一个Region的一个Store中选择部分HFile文件进行合并。

合并原理是，先从这些待合并的数据文件中依次读出KeyValue，再由小到大排序后写入一个新的文件。

之后，这个新生成的文件就会取代之前已合并的所有文件对外提供服务。

- Minor Compaction：指选取部分小的、相邻的HFile，将它们合并成一个更大的HFile。

- Major Compaction：指将一个Store中所有的HFile合并成一个HFile，这个过程还会完全清理三类无意义数据：被删除的数据、TTL过期数据、版本号超过设定版本号的数据。

作用：

- 合并小文件，减少文件数，稳定随机读延迟。文件速率多，IO次数也多。
- 提高数据的本地化率。
  - **Data Locality：region的HFile位于本地的百分比**
  - 合并小文件的同时读取远程DN上的数据写入大文件，合并的大文件会在本地保留一个副本。
  - 地化率越高，在HDFS上访问数据时延迟就越小；相反，本地化率越低，访问数据就可能大概率需要通过网络访问，延迟比较大。
- 清除无效数据，减少数据存储量。

Compaction使用短时间的IO消耗以及带宽消耗换取后续查询的低延迟。



#### REF

- [HBase1.x优化：数据本地化率？](https://my.oschina.net/u/2380815/blog/4453969)





## 6. Region负载均衡(迁移，合并，分裂)

### 6.1 Rowkey设计

HBase 中的行按行按**字典顺序排序**。对于顺序扫描有利。

但是Rowkey设计不好，导致热点问题。（大量客户端流量包括读取，写入或其他操作指向群集的一个节点或仅几个节点）

打散热点的rowkey设计方式：

- 添加随机前缀

  - 也被叫做slating加盐，引用自加密技术

  ```
  foo0001
  foo0002
  foo0003
  foo0004
  -> 分成4个区域，新增记录随机前缀
  a-foo0003
  b-foo0001
  c-foo0004
  d-foo0002 
  写快，扫描开销增加
  ```

- 哈希

  - 相同行始终在一个region，一定程度维持有序

- 反转固定宽度或数字行键

  - 例如最低位，改到第一个。会牺牲排序属性，读取时每次要扫描所有的region。

在维持有序性和分散热点之间取得tradoff。

更多[table设计](https://communities.intel.com/community/itpeernetwork/datastack/blog/2013/11/10/discussion-on-designing-hbase-tables)，[slated表（分桶）](https://phoenix.apache.org/salted.html)，[HBASE-11682 Explain hotspotting](https://issues.apache.org/jira/browse/HBASE-11682)

### 6.2 列族数量

官方推荐使用尽量少，一般1个。

> 在数据访问通常是列作用域的情况下，才引入第二和第三列族;即您查询一个列族或另一个列族，但通常不是同时查询两个列族。

原因是flush，压缩机制是以region为单位的。

一个列族突然插入大量数据，需要进行flush和压缩，其他未修改的列族也必须进行，产生没有必要的IO。

并且一个列族数量很多，另一个列族数据量很小时，小数据量的列族被分散到大量的region中，导致该列族的大规模扫描性能降低。



## 7.宕机恢复



## 8. 副本同步(跨集群)

基本思路利用WAL logging 同步到备集群，避免主集群宕机，备集群丢失数据。（对比MySQL同步）



#### REF

- [HBASE-20422](https://issues.apache.org/jira/browse/HBASE-20422)
- [HBase Synchronous Replication](https://docs.google.com/document/d/193D3aOxD-muPIZuQfI4Zo3_qg6-Nepeu_kraYJVQkiE/edit#) 方案设计



## 9.备份恢复



#### REF

- [备份和恢复指令](http://hbase.org.cn/docs/113.html)





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


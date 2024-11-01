# Lucene 笔记

## 1.概念

### 1.1 索引 index

类似数据库中的表，但是没有shcema的约束。存储任意类型的文档

### 1.2 文档 document

类似数据库中的行，文档数据库内的文档。

具有唯一的ID，docID。

### 1.3 字段(域) Field

一个Document会由一个或多个Field组成，Field是Lucene中**数据索引**（非1.1的索引）的最小定义单位。

支持的类型：

- String
- Text
- Long
- Numeric

Lucene根据Field的类型FieldType，对数据使用不同的索引方式。

### 1.4 词项Term和Term Dictionary

Lucene中索引和搜索的最小单位，一个Field会由一个或多个Term组成，Term是由Field经过Analyzer（分词）产生。Term是二元组（字段名，词token）。

Term Dictionary即Term词典，根据条件查找Term的基本索引。

每个Term 映射有序的docID列表（内存数据结构skiplist，便于多个term的倒排链合并时，跳过无效doc）。

### 1.5 段Segement

一个Index会由一个或多个Segement构成。一个segement，类似一颗lsm-tree，提供近实时查询。

Lucene中的数据写入会先写内存的一个Buffer（类似LSM的MemTable，但是不可读），当Buffer内数据到一定量后会被flush成一个Segment，每个Segment有自己独立的索引，可独立被查询，但数据永远不能被更改。

### 1.6 DocValues

DocValues是Lucene在构建索引时，会额外建立一个有序的基于document => field value的映射列表；（正向索引） 

DocValues 提供了对一系列docId所对应的一个filed的一组值（一列数据），根据field类型()可以使用不同类型的DocValues。不分词，正排索引结构，面向列式存储格式。


- [Lucene源码解析——DocValue存储方式](https://zhuanlan.zhihu.com/p/384487150) 推荐

  - sorted并不是说将field value排序后，存储value -> docid的映射（这个就是mysql的索引了!），而是另外一层意思， 对于SortedNumericDocValue来说就是一个field中的多个值是有序的， 而对于SortedDocValues来说，这个sorted是指将字符串按照字典顺序排序转成的value
  - 但 NumericDocValues，或者SortedNumericDocValues 所使用的编码方式（v - min）/gcd 缩减v的值域范围，再通过bit-packing缩减需要存储的bits来进行存储压缩，实际对于float,double类型类型，基本不工作。


  - SortedDocValues 
  - SortedSetDocValues

-  [Lucene源码解析——StoredField存储方式](https://zhuanlan.zhihu.com/p/384486147)
  - ZFloat：Float类型，会尝试精简编码成int
- [BinaryDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0412/49.html) 
  - 二进制类型值对应不同的codes最大值可能超过32766字节
- [SortedDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0219/34.html)
  - 字符串+单值， termID 原始docid顺序
  - 将字符串按照字典序排序后termID的顺序 sortedValues， Ord -> TermID
  - 字典大小顺序Ord， ordMap：TermID->Ord 数组，下标是termID,值是Ord，用DirectWriter压缩无序列表
  - TermDict：该字段下所有的term，顺序的，采取前缀压缩
  - TermIndex：稀疏term索引
- [SortedSetDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0412/48.html)
  - 同一个文档同一个域可以存储多值域的docvalue值，但返回时，仅仅只能返回多值域的第一个docvalue
  - 比SortedDocValues额外多OrdAddress字段
- [NumericDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0409/46.html)
  - 单个数值类型的docvalue主要包括（int，long，float，double）
  - docid->value
- [SortedNumericDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0410/47.html)
  - 存储数值类型的有序数组列表   数值或日期或枚举字段+多值
  - docid->values， 并且 values 有序
  - 有序数组压缩：DirectMonotonicWriter
- [BinaryDocValues-8.7.0](https://www.amazingkoala.com.cn/Lucene/DocValues/2020/1121/179.html)



缩略词dvd(DocValueData)，dvm(DocValueMeta)


- [浅谈Lucene中的DocValues](https://cloud.tencent.com/developer/article/1122277)
- [lucene DocValues之NumericDocValues](https://zhuanlan.zhihu.com/p/631980445)
- [lucene DocValues之SortedDocValues](https://zhuanlan.zhihu.com/p/654522546)

- [lucene 编码技术 - DirectWriter](https://zhuanlan.zhihu.com/p/588900849)
  - 将 long[] 型数据集编码存储到 byte[] 使用 固定bits编码（bit-packing） bitPerValue

- [DocValues](https://www.amazingkoala.com.cn/tags/DocValues/)





### 1.7 StoredField & StoreValues （行存）
 
StoreValues 提供行存格式。 比如`_source` 字段存储原始数据。


- [Lucene StoredField 原理](https://zhuanlan.zhihu.com/p/713532844)

### 1.8 InvertedIndex 倒排索引



## 2. 原理

### 2.1 查询原理

- FST：保存term字典，可以在FST上实现单Term、Term范围、Term前缀和通配符查询等。
- 倒排链：保存了每个term对应的docId的列表，采用skipList的结构保存，用于快速跳跃。
- BKD-Tree：BKD-Tree是一种保存多维空间点的数据结构，用于数值类型(包括空间点)的快速查找。
- DocValues：基于docId的列式存储，由于列式存储的特点，可以有效提升排序聚合的性能。

两阶段搜索

- 通过给定的Term的条件找到所有Doc的DocId列表
- 根据DocId查找Doc


经验：

从 lucene 读取 5w/s



- [https://zhuanlan.zhihu.com/p/671225495](Lucene 倒排索引之 FST)
  - 倒排索引的实现，HashMap -> Trie 前缀树 -> FST（Finite State Transducer）
  - FST，不但能共享前缀还能共享后缀。不但能判断查找的key是否存在，还能给出响应的输入output。

## System requirements 
- Lucene 9.0 requires JDK 11 or newer

- Lucene 8.11.3  JDK 8 or greater

## 文件格式说明：

- 域数据文件 (.fdx 和 .fdt)：.fdt文件存储了文档中域（Field）的具体内容，而.fdx文件作为.fdt文件的索引，记录了文档在.fdt文件中的偏移位置，以便快速定位
- 词项字典文件 (.tis 和 .tii)：这些文件构成了词典，包含了段中所有词项（Term）的集合，并按字典顺序排序，它们是实现倒排索引的基础
- 词频文件 (.frq)：此文件存储了每个词项在文档中的频率，即文档中出现多少次该词项
- 词位置文件 (.prx)：.prx文件存储了词项在文档中出现的位置信息

- 删除文档文件 (.del)：这个文件记录了已经被删除的文档，但实际上文档数据仍然保留在索引中，直到索引优化(Optimize)操作发生

- Compound File (.cfs 或 .cfe)：复合文件格式将多个文件合并为一个文件，以减少文件句柄的使用并提高效率

- .dvd文件存储了DocValues的数据，与之配套的.dvm文件存储了元数据，用于解析.dvd文件中的数据。每个DocValues字段的数据和元数据文件是分开存储的

https://lucene.apache.org/core/9_10_0/core/org/apache/lucene/codecs/lucene99/package-summary.html#package.description


## REF

- [Apache lucene](https://lucene.apache.org/)
- [Lucene解析 - 基本概念](https://zhuanlan.zhihu.com/p/35469104)
- [基于Lucene查询原理分析Elasticsearch的性能](https://zhuanlan.zhihu.com/p/47951652)
- [Lucene底层架构-dvm-dvm构建过程](https://kkewwei.github.io/elasticsearch_learning/2019/11/15/Lucene%E5%BA%95%E5%B1%82%E6%9E%B6%E6%9E%84-dvm-dvm%E6%9E%84%E5%BB%BA%E8%BF%87%E7%A8%8B/)


- [深度解析 Lucene 轻量级全文索引实现原理](https://cloud.tencent.com/developer/news/841587)

扩展材料：

- 原理
  - [Lucene 查询原理](https://zhuanlan.zhihu.com/p/35814539)
  - [Elasticsearch内核解析 - 数据模型篇](https://zhuanlan.zhihu.com/p/34680841)
  - [剖析Elasticsearch的IndexSorting:一种查询性能优化利器](https://zhuanlan.zhihu.com/p/49206974)
    - 预排序字段，类似二级索引，docID的顺序与IndexSorting的顺序一致
    - 优点：
      - 结果有序，减少返回数据
      - 其他列特征相似，从而提高数据压缩率
  - [Lucene核心技术](https://www.amazingkoala.com.cn/Lucene/2019/1205/115.html) lucene 博客源码系列
    - [github: lucene-7.5.0](https://github.com/LuXugang/Lucene-7.5.0)
    - [索引文件生成（一）](https://www.amazingkoala.com.cn/Lucene/Index/2019/1226/121.html)
  - [lucene 8.6.2](https://kkewwei.github.io/elasticsearch_learning/categories/Lucene/) 中文博客
  - [Elasticsearch Lucene 数据写入原理 | ES 核心篇](https://www.cnblogs.com/Alandre/p/11358954.html)

- 架构
  - [Elasticsearch分布式一致性原理剖析(一)-节点篇](https://zhuanlan.zhihu.com/p/34858035)
  - [Elasticsearch分布式一致性原理剖析(二)-Meta篇](https://zhuanlan.zhihu.com/p/35283785)
  - [Elasticsearch分布式一致性原理剖析(三)-Data篇](https://zhuanlan.zhihu.com/p/35285514)
    - ·先写Lucene（内存数据），再写translog  （commit log），避免写luncene失败
- 源码分析
  - [Lucene解析 - IndexWriter](https://zhuanlan.zhihu.com/p/35795070)
  - [Lucene的部分源码阅读](https://zhuanlan.zhihu.com/p/367391355)
  - [从源码看 Lucene 的文档写入流程](https://juejin.cn/post/7137453263795781639) 

- 开发
  - [ZSTD Compressor support in Lucene [LUCENE-8739]](https://github.com/apache/lucene/issues/9784) 关于zstd 压缩的支持，主要一直未成功原因是 zstd 是C++，管理者 不想在内核引入 jni 依赖，glibc等可移植问题
    - 不过facebook 也开源了 [airlift/aircompressor](https://github.com/airlift/aircompressor) 支持纯java的 zstd 声称比jni，jna方式更快，但是测试下来还是要比jni方式慢一倍


# Lucene 笔记

## 1.概念

### 1.1 索引 index

类似数据库中的表，但是没有shcema的约束。存储任意类型的文档

### 1.2 文档 document

类似数据库中的行，文档数据库内的文档。

具有唯一的ID，docID。

### 1.3 字段 Field

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

DocValues 提供了对一系列docId所对应的一个filed的一组值（一列数据），根据field类型()可以使用不同类型的DocValues。不分词，正排索引结构，面向列式存储格式。

- [BinaryDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0412/49.html) 
  - 二进制类型值对应不同的codes最大值可能超过32766字节
- [SortedDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0219/34.html)
  - 字符串+单值
- [SortedSetDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0412/48.html)
  - 同一个文档同一个域可以存储多值域的docvalue值，但返回时，仅仅只能返回多值域的第一个docvalue
- [NumericDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0409/46.html)
  - 单个数值类型的docvalue主要包括（int，long，float，double）
- [SortedNumericDocValues](https://www.amazingkoala.com.cn/Lucene/DocValues/2019/0410/47.html)
  - 存储数值类型的有序数组列表   数值或日期或枚举字段+多值
- [BinaryDocValues-8.7.0](https://www.amazingkoala.com.cn/Lucene/DocValues/2020/1121/179.html)

缩略词dvd(DocValueData)，dvm(DocValueMeta)

StoreValues 提供行存格式。 比如`_source` 字段存储原始数据。

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


## REF

- [Apache lucene](https://lucene.apache.org/)
- [Lucene解析 - 基本概念](https://zhuanlan.zhihu.com/p/35469104)
- [基于Lucene查询原理分析Elasticsearch的性能](https://zhuanlan.zhihu.com/p/47951652)
- [Lucene底层架构-dvm-dvm构建过程](https://kkewwei.github.io/elasticsearch_learning/2019/11/15/Lucene%E5%BA%95%E5%B1%82%E6%9E%B6%E6%9E%84-dvm-dvm%E6%9E%84%E5%BB%BA%E8%BF%87%E7%A8%8B/)

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
- 架构
  - [Elasticsearch分布式一致性原理剖析(一)-节点篇](https://zhuanlan.zhihu.com/p/34858035)
  - [Elasticsearch分布式一致性原理剖析(二)-Meta篇](https://zhuanlan.zhihu.com/p/35283785)
  - [Elasticsearch分布式一致性原理剖析(三)-Data篇](https://zhuanlan.zhihu.com/p/35285514)
    - ·先写Lucene（内存数据），再写translog  （commit log），避免写luncene失败
- 源码分析
  - [Lucene解析 - IndexWriter](https://zhuanlan.zhihu.com/p/35795070)
  - [Lucene的部分源码阅读](https://zhuanlan.zhihu.com/p/367391355)
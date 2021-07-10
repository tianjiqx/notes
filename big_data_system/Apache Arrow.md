# Apache Arrow

**概念**：

Apache Arrow 是一个跨语言的内存数据开发平台，用于构建处理和传输大型数据集的高性能应用程序。它旨在提高分析算法的性能以及**将数据从一种系统或编程语言转移到另一种系统或编程语言的效率**。

Apache Arrow 的一个关键组件是其**内存中列格式**，这是一种标准化的、与语言无关的规范，用于表示内存中结构化的、类似表格的数据集。支持平面，或者嵌套的自定义数据格式。

它还提供计算库和零拷贝流消息传递和进程间通信。



**柱状格式**：

- 扫描和迭代大块数据时最大限度地提高效率
- SIMD向量化操作

![](apache-arrow笔记图片/simd.png)

**节省SerDe**：

没有标准的列数据格式，每种数据库和语言都必须实现自己的内部数据格式，之前数据的相互联邦需要做昂贵的SerDe。还可能需要重写通用的算法（如果只是运算，这点感觉在SerDe成通用的数据类型如java object后，可以免除，但是代价是，必须经过SerDe后运算。这里应该是指原生系统而言，自己需要重复开发）。

Apache Arrow 由十多个开源项目开发者支持，包含 Calcite, Cassandra, Drill, Hadoop, HBase, Ibis, Impala, Kudu, Pandas, Parquet, Phoenix, Spark, 和 Storm等。

使用或支持 Arrow 的系统（目前更多的是为大数据分析系统OLAP）可以在它们之间以很少甚至免费的成本传输数据。

标准化的内存格式促进了算法库的重用，甚至可以跨语言重用。

![](apache-arrow笔记图片/copy.png)

![](apache-arrow笔记图片/shared.png)

**Arrow lib库**：

Arrow 项目包含的库使您能够以多种语言处理 Arrow 柱状格式的数据。



## REF

- [Apache Arrow官方](https://arrow.apache.org/overview/)

- [Apache Arrow 内存数据](https://www.cnblogs.com/smartloli/p/6367719.html)

- [TiDB 源码阅读系列文章（十）Chunk 和执行框架简介](https://pingcap.com/blog-cn/tidb-source-code-reading-10/#tidb-%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%E7%B3%BB%E5%88%97%E6%96%87%E7%AB%A0%E5%8D%81chunk-%E5%92%8C%E6%89%A7%E8%A1%8C%E6%A1%86%E6%9E%B6%E7%AE%80%E4%BB%8B)







- [查询编译综述](https://zhuanlan.zhihu.com/p/60965109)














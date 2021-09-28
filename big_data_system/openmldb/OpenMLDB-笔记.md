# OpenMLDB-笔记

## 1. 简介

背景，论文基本原理相关，见[大数据系统-鉴赏](https://github.com/tianjiqx/notes/blob/master/big_data_system/%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%B3%BB%E7%BB%9F-%E9%89%B4%E8%B5%8F.md) 22 节。 





分析源码版本（2021.09.28）：

`432da3afbed240eb0b8d0571c05f233b1a5a1cd4`





## 2. 架构

![](openmldb图片/openmldb_architecture.png)

- 执行引擎Hybridse
  - 实时+ 批处理
- 存储引擎
  - tablet  server  存储服务
- 元信息管理
  - nameserver
    - 管理tablet 的元信息，表schema等服务
  - zookeeper
    - 先猜测是提供一致性，为nameserver选主
- api server
  - 提供 resutful api 访问nameserver





## 3.  执行引擎HybridSE

HybridSE(Hybrid SQL Engine)是基于C++和LLVM实现的高性能混合SQL执行引擎，为AI应用、OLAD数据库、HTAP系统、SparkSQL、Flink Streaming SQL等提供一致性的SQL加速优化。

![](openmldb图片/HybridSE.png)



源码结构：

- `docker`  HybridSQL 的 docker image 构建脚本
- `examples`
  - 包含基于HybridSE实现的内存表SQL引擎toydb
- `include` 部分模块头文件定义（`src` 也有有文件）
- `java`  java sdk，当前内容基本没有
- `python` python sdk，同样为应用开发人员的sdk，内容暂时也基本没有，可能实现在`src/sdk`
- `tools`  打包测试相关工具，具体功能看该目录下的readme
  - 编译检查
  - 编译，功能测试
  - 集成测试，性能测试
- `src` 主要的源代码



(当前一些文档连接，似乎由于项目名更改，已经无法访问； `zetasql/parser/parser.h` 也暂时未找到定义)



## REF

- [github: openMLDB](https://github.com/4paradigm/OpenMLDB)


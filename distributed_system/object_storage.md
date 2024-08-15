
# 对象存储

## 概念

对象存储是一种存储架构，用于处理非结构化数据。它以对象为单位来存储数据，每个对象包括数据本身（即实际的内容）、元数据（描述数据的信息）以及一个全局唯一的标识符。

对象存储系统通常用于存储图片、音频、视频、备份文件等大量的非结构化数据。
这种存储方式与传统的文件存储和块存储有显著的不同。文件存储以文件系统为基础，数据被组织在文件夹中，而块存储则将数据存储在固定大小的块中，这些块可以被随机读写。对象存储则更加灵活，可以更容易地扩展，并且适合存储大量的数据。



## AWS S3（Simple Storage Service）


## CubeFS

## MinIO


## 支持面向对象存储的系统

- prestro 借助 Hive 连接器，读取和写入存储在 S3 上的表
    - trino 增加 s3 文件系统支持



## REF


- [[VLDB'22] CloudJump: 存储层上云优化](http://47.241.45.216/2023/01/01/VLDB-22-CloudJump-optimizing-cloud-databases-for-cloud-storages/)


- [CubeFS 文件系统架构 设计及应用｜Data Infra 研究社第20期](https://www.bilibili.com/video/BV1XCafe8ECS/)

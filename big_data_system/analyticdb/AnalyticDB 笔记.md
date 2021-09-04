# AnalyticDB 笔记

## 1. 背景

ADB的挑战/问题：

- 实时分析
  - 在线化和高可用
- 数据规模
  - PB级别的分析负载，万级表数量，万亿级数据量
- 复杂查询
  - 全表扫描、点查、多表关联、多条件组合
  - 混合负载
    - 数据加工处理
    - 高并发低延时的交互式查询
- 复杂数据类型
  - 文本、json串、向量和其他多媒体资源的快速检索
  - 融合分析
- 高写入吞吐
  - 低延迟查询时，同时每秒数百万行在线写入请求



ADB主要创新：

- 高效索引管理
  - 异步的方式维护所有的列索引
  - 基于运行时过滤比的索引路径选择
- 存储结构
  - 混合行列的数据布局
  - 支持OLAP，点查询
- 读写分离架构
  - 读节点和写节点，独立扩容
  - 版本验证机制
- 存储感知的SQL优化器和执行引擎
  - 向量化执行



性能：

100万亿行记录，10PB+大小

10m+ w  100k+ r /s 

亚秒级的复杂查询。



## 2. 系统设计

![](AnalyticDB笔记图片/Snipaste_2021-09-04_22-12-39.png)

- Pangu 分布式存储系统
  - 写节点会将写请求的数据刷到盘古上进行持久化
- Fuxi 资源管理和作业调度
  - 计算任务的异步调度执行
- ADB
  - JDBC/ODBC接口
  - Coordinator 协调者
    - 接收客户端查询请求，并分发到读写节点
  - 写节点（计算）
    - dml
  - 读节点（计算）
    - select

![](AnalyticDB笔记图片/Snipaste_2021-09-04_22-13-14.png)



读写分离：

- 避免资源竞争
  - 资源？



表分区：

- 一级分区
  - 节点
  - 分区键：高基数（cardinality）的列
  - 二级分区
    - 节点内的分区
    - 具有最大分区数
    - 分区键：时间列（天、周或月）



## 3. 存储



## 4. 优化器和执行引擎



## 5. 实验





## REF

- Zhan, C., Su, M., Wei, C., Peng, X., Lin, L., Wang, S., … Chai, C. (2018). AnalyticDB: Real-time OLAP database system at Alibaba Cloud. Proceedings of the VLDB Endowment, 12(12), 2059–2070. https://doi.org/10.14778/3352063.3352124
- [前沿 | VLDB论文解读：阿里云超大规模实时分析型数据库AnalyticDB](https://developer.aliyun.com/article/716784) 论文补充说明
- [VLDB 2019 笔记: AnalyticDB: Real-time OLAP Database System at Alibaba Cloud](https://www.jianshu.com/p/342a059af224)
- [Paper翻译 AnalyticDB Real-time OLAP Database System at Alibaba Cloud](https://changbo.tech/blog/e3ee66c7.html)
- [如何通过数据仓库实现湖仓一体数据分析？](https://mp.weixin.qq.com/s/Cy5UIpGg0oGxvU5nonM9CA)
- [关于AnalyticDB 3.0的调研和分析](https://blog.microdba.com/database/2020/01/15/about-aliyun-analyticdb-for-mysql/)


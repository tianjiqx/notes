# TiDB v5.1.0 查询优化器源码分析-笔记

## 1. 配置

- 编辑器：vim。

- vim 配置：

  参考个人workspace项目的[.vimrc](https://github.com/tianjiqx/workspace/blob/master/.vimrc)文件。 快捷键使用参考[vim-go插件使用](https://github.com/tianjiqx/notes/blob/master/tools-tutorial/vim-go%E6%8F%92%E4%BB%B6%E4%BD%BF%E7%94%A8.md)

- TiDB源码版本tag v5.1.0 (2021.6.23)

  `commit 8acd5c88471cb7b4d4c4a8ed73b4d53d6833f13e`
  
- 编译问题

  - make失败，go包管理网址无法访问：proxy.golang.org，使用国内代理`go env -w GOPROXY=https:*//goproxy.cn*`



## 2.SQL执行流程

还是从SQL执行流程开始。由于时间太久，知道以前官方文档的源码分析是否过时，先网络搜一下别人的源码分析。根据知乎院长的TiDB学习笔记，可以看到，距离3年前分析TiDB2.1时，SQL连接处理入口还是没变，在server/server.go的onConn()开始。

- `func (s *Server) onConn(conn *clientConn)`
  - `func (cc *clientConn) Run(ctx context.Context) `



## 3.Cascades 模型的优化器

**动机：**

- 传统多阶段优化，逻辑优化的聚合下推、聚合上拉、子查询展开等并不是总是有益的
- 可扩展性差，即使都是有益的场景规则，很难添加新规则，需要仔细考虑优化规则的应用顺序，并且需要丰富的优化经验，发现各种优化规则
- 代价模型绑定，物理存储引擎的扩展，进行物理优化的扩展性差。



**Cascades 模型的观点：**

- 自顶向下的探索所有可能计算代价+memo 记录子表达式避免重复
- 





## 4.统计信息推导（Stats Derivation）

原始统计信息，是收集每张表的总行数，全局/分片(region)的各列的不同值个数，列的min，max值。高频值的选择率（单值查询，count min sketch, 源码对象NewCMSketch）(查看tidb源码StatsInfo只有Cardinality是单个map，只是topN）。GroupNDV是tidb对多列组合的不同值个数的统计（看起来是全局的）。

列直方图(Histogram,histogram.go)，具有列id，不同值个数，null值个数，分桶边界，桶（行数，不同值个数，重复次数）



统计信息推导，是指经过filter，join之后的统计信息估计。主要的内容是ndv值的推导。用ndv值估计连接结果大小。

- filter：列的敏感性，非求ndv列的选择率，独立分布均匀假设。（tidb也参考SQL server调整估计限制最多4次）

- join：
  - 基于region之间的笛卡尔积计算方式进行join，每两个region的连接可以视作表的连接，最后统计总的连接大小。
  - tidb：基于全局直方图信息的join，大小估计
    - region 边界对齐——假设均匀分布
    - min (NDV1,NDV2) （内连接）
    - 外连接处理



TiDB 统计信息支持全量、采样收集，时间列的增量收集。

（全量，统计信息更新代价？）



## REF

- [TiDB源码学习笔记：启动TiDB](https://zhuanlan.zhihu.com/p/304036138)
- [TiDB的后花园 - 知乎专栏](https://www.zhihu.com/column/newsql) 
- [SQL 性能调优](https://docs.pingcap.com/zh/tidb/stable/sql-tuning-overview) 
- [提案：基于 Volcano/Cascades 模型的 SQL Planner](https://github.com/pingcap/tidb/blob/master/docs/design/2018-08-29-new-planner.md)
- [提案：维护计划中的统计信息(直方图的统计信息推导)](https://github.com/pingcap/tidb/blob/master/docs/design/2018-09-04-histograms-in-plan.md)
- [提案：join 重排序设计](https://github.com/pingcap/tidb/blob/master/docs/design/2018-10-20-join-reorder-dp-v1.md) 推荐
- [TiDB 统计信息简介 ](https://docs.pingcap.com/zh/tidb/stable/statistics#%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF%E7%AE%80%E4%BB%8B)










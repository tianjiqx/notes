# 性能监控(profiling)

[TOC]

## 1. 背景

profiling用于性能监控，分析查询负载的瓶颈，例如记录数据库SQL各个算子的用时，大数据系统的Job，Task用时时间。



## 2. profiling实现

### 2.1 OceanBase

ObMonitorNode* op_monitor_info_;



### 2.2 spark



### 2.3 TiDB



### 2.4 PolarDB





### 2.5 crate

CrateDB 是一个分布式 SQL 数据库，面向机器数据的存储和分析。（Java）

特性：

- SQL
- Lucene



create对查询的metrics监控，类似于spark。

`ProfilingContext ` profiling上下文

- 存储了各个阶段的执行时间。
- 跨越analyzer, planner, executor层
- 成员变量
  - `HashMap<String, Double> durationInMSByTimer` 
    - Key：阶段，value：用时
    - `io.crate.profile.Timer` 对象代表一个节点的用时
  - `List<QueryProfiler> profilers` 记录ES查询执行的profiler信息
    - `QueryProfiler` 继承`org.elasticsearch.search.profile.AbstractProfileBreakdown`
      - 记录查询执行期间可能发生的各种操作的计时记录



`io.crate.execution.jobs.RootTask`

- 创建RootTask时，传入`ProfilingContext ` ，通过事件监听器，监听task开始和完成任务的时间，并放入到`ProfilingContext ` 



## REF

- [TiDB 重要监控指标详解](https://docs.pingcap.com/zh/tidb/v2.1/grafana-tidb-dashboard#tidb-%E9%87%8D%E8%A6%81%E7%9B%91%E6%8E%A7%E6%8C%87%E6%A0%87%E8%AF%A6%E8%A7%A3)
- [TiDB in action: 1.5 限制 SQL 内存使用和执行时间](https://book.tidb.io/session3/chapter1/memory-quota-execution-time-limit.html)
- [TiDB 写入慢流程排查系列（三）— TiDB Server 写入流程](https://asktug.com/t/topic/68070)
- [github:crate ](git@github.com:crate/crate.git)


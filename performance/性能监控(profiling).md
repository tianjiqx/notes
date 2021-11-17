# 性能监控(profiling)

[TOC]

## 1. 背景

profiling（剖析）用于性能，资源的监控，主要用来

- CPUProfiling 分析查询负载的瓶颈
  - 例如记录数据库SQL各个算子的用时，大数据系统的Job，Task用时时间
- Headp Profiling 分析内存使用，定位于排查内存泄漏



## 2. Profiling原理

### 2.1 CPU Profiling

linux 上cpu cpu分析工具

分类：

- **Instrumentation** 检测
  - 在每个routine的开始和结束处插入特殊代码来记录routine何时开始和结束
  - 方式
    - 源代码修改
    - 二进制
      - 在内存中将检测插入到可执行代码
  - 优点
    - 实际时间
  - 缺点
    - 检测代码本身的开销，容易干扰于短和高频的routine
  - 工具
    - gprof（检测和采样混合），gperftools（多线程，google）
- **Sampling** 采样
  - 记录操作系统定期中断CPU执行进程切换时执行的指令，并将记录的执行点与链接过程中的routine和源代码相关联，显示应用程序运行期间执行routine和源代码行的频率（火焰图）
    - stack trace + statistics
  - 优点
    - 无需修改代码
    - 运行开销很小
  - 缺点
    - 统计近似值而不是实际时间
  - 工具
    - perf



### 2.2 Heap Profiling

内存Profiling与CPU Profiling类似，同样可以根据stack trace + statistics或者统计真实申请的方式来统计各函数的内存分配。

由于内存分配是很频繁的操作，一种方式（Golang）是按一定粒度大小（512K）进行采样。（为了解决采样bais问题，粒度大小可以设置为服从正太分布的随机值）

另一种方式（C/C++），创建内存分配器对象，从更底层的内存分配池获取空闲缓存块（块设置不同大小的粒度，1K，2M等）进行分配和回收，记录每个类或者功能模块，独立申请的内存空间大小，定期或者接受信号时，打印各功能模块的内存使用。



## 3. 数据库Profiling实现

### 3.1 OceanBase

时间统计对象

```C++
// 算子监控
ObMonitorNode  
  int64_t open_time_;
  int64_t first_row_time_;
  int64_t last_row_time_;
  int64_t close_time_;
  int64_t rescan_times_;
  int64_t output_row_count_;
  int64_t memory_used_;
  int64_t disk_read_count_;
```



ObPhyOperator

- 成员
  - ObMonitorNode
  -  lib::MemoryContext
- 方法
  - get_next_row中设置
    - op_monitor_info\_.first_row_time_
    - op_monitor_info\_.output_row_count_
    - op_monitor_info\_.last_row_time_
  - close
    - op_monitor_info\_close_time_



`ObOpSpec::create_operator_recursive()` 创建算子时，设置open_time_

CREATE_PHY_OPERATOR_CTX 创建算子上下文时，设置open_time_



ObMergeJoin

- 继承OBJoin
  - 继承ObDoubleChildrenPhyOperator
    - 继承ObPhyOperator





`ObExecTimestamp` 记录了计划执行过程各个时间戳

- ExecType { InvalidType = 0, MpQuery, InnerSql, RpcProcessor, PLSql }
- rpc_send_ts_
- receive_ts_ 接收到请求时间
- enter_queue_ts_ 
- run_ts_ 解码后开始执行时间
- before_process_ts_
- single_process_ts_ 单独sql的开始执行是回见
- process_executor_ts_ 开始执行时间
- executor_end_ts_

`ObReqTimestamp` 



`ObAuditRecordData` 审计日志

- `ObExecTimestamp`
- `ObExecRecord`



`sql/executor/ob_bkgd_dist_task.h`

`ObDistExecuteBaseP`

- RpcProcessor类型
- process_timestamp_
  - ` ObExecStatUtils::record_exec_timestamp()`
- exec_start_timestamp_
- exec_end_timestamp_

`ObBKGDDistTask` 后台执行的分布式task

- create_time_us_ 任务创建时间
- ObDistTaskProcessor  继承ObDistExecuteBaseP



总结：

- 节点算子记录，算子的执行各个时间戳
- 分布式计划Task，也在Task对象中维持各个时间戳属性
- 最后基于时间戳，计算各个阶段的执行时间



### 3.2 spark



### 3.3 TiDB

### 3.3.1 Heap Profiling

TiDB组件

方式：基于采样

工具：

- go pprof



sysbench 结果：

- 512k 采样记录的性能损耗基本都在 1% 以内
- 全记录TPS/QPS 缩水了 20 倍，P95 延迟增加了 30 倍

TiKV组件

方式：基于采样

工具：

- jemalloc （rust）

go-ycsb 结果：

- OPS 相较默认内存分配器下降了 4% 左右，P99 延迟线上升了 10% 左右
  - tcmalloc与jemalloc性能类似



### 3.4 PolarDB



### 3.5 crate

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
    - Key：阶段名称，value：用时
    - `io.crate.profile.Timer` 对象代表一个节点的用时
  - `List<QueryProfiler> profilers` 记录ES查询执行的profiler信息
    - `QueryProfiler` 继承`org.elasticsearch.search.profile.AbstractProfileBreakdown`
      - 记录查询执行期间可能发生的各种操作的计时记录



`io.crate.execution.jobs.RootTask`

- 创建RootTask时，传入`ProfilingContext ` ，通过事件监听器，监听task开始和完成任务的时间，并放入到`ProfilingContext ` 



`MemoryManager` 内存管理，分配ByteBuf

- 堆内
- 堆外



总结：

- `ProfilingContext `  对象记录整个计划大的阶段时间
- `io.crate.profile.Timer` 对象记录一个时间区间，开始和结束
- Task为粒度，记录执行时间
- 基于Future回调，设置监听器完成时间。



## REF

- [TiDB 重要监控指标详解](https://docs.pingcap.com/zh/tidb/v2.1/grafana-tidb-dashboard#tidb-%E9%87%8D%E8%A6%81%E7%9B%91%E6%8E%A7%E6%8C%87%E6%A0%87%E8%AF%A6%E8%A7%A3)
- [TiDB in action: 1.5 限制 SQL 内存使用和执行时间](https://book.tidb.io/session3/chapter1/memory-quota-execution-time-limit.html)
- [TiDB 写入慢流程排查系列（三）— TiDB Server 写入流程](https://asktug.com/t/topic/68070)
- [github:crate ](git@github.com:crate/crate.git)
- [CPU Profiling Tools on Linux](http://euccas.github.io/blog/20170827/cpu-profiling-tools-on-linux.html)
- [内存泄漏的定位与排查：Heap Profiling 原理解析](https://pingcap.com/zh/blog/an-explanation-of-the-heap-profiling-principle?utm_source=wechat&utm_medium=social&utm_campaign=heap-profiling)
- [Brendan Gregg perf](https://www.brendangregg.com/perf.html) 性能之巅作者博客



扩展材料：

- [[译] 使用 Linux tracepoint、perf 和 eBPF 跟踪数据包 (2017)](https://arthurchiao.art/blog/trace-packet-with-tracepoint-perf-ebpf-zh/)
- [[译] Cilium：BPF 和 XDP 参考指南（2021）](https://arthurchiao.art/blog/cilium-bpf-xdp-reference-guide-zh/)


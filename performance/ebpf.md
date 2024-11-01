# eBPF


## Continuous Profiling 持续性能分析

- SPT - System Profiling Tools


- LPT - Language Profiling Tools
    - java
        - JVM Profiling Tools
            - Async-profiler 
            - JProfiler

    - go

DataDog对类型的划分：https://docs.datadoghq.com/profiler/profile_types/


- On-CPU: where threads are spending time running on-CPU.
- Off-CPU: where time is spent waiting while blocked on I/O, locks, timers, paging/swapping, etc. 


[otel对类型的划分](https://github.com/open-telemetry/oteps/blob/main/text/profiles/0239-profiles-data-model.md#profile-types)




## REF

- [eBPF 文档](https://ebpf.io/zh-hans/what-is-ebpf/)

- [deepflow](https://github.com/deepflowio/deepflow/tree/main) DeepFlow 基于 eBPF 实现了零侵扰（Zero Code）的指标、分布式追踪、调用日志、函数剖析数据采集，并结合智能标签（SmartEncoding）技术实现了所有观测数据的全栈（Full Stack）关联和高效存取。
    - [SmartEncoding](https://deepflow.io/docs/zh/features/auto-tagging/smart-encoding/) 看起来，SmartEncoding其实就是tagId 



- [DataDog profiling](https://app.datadoghq.com/profiling/explorer)
- [观测云](https://docs.guance.com/best-practices/monitoring/async-profiler/)

- blogs:
    - [可观测可回溯 | Continuous Profiling 实践解析](https://www.cnblogs.com/alisystemsoftware/p/16836933.html)

    - [eBPF 零侵扰分布式追踪 3 分钟锁定 Java 程序 I/O 线程阻塞](https://www.deepflow.io/blog/zh/081-locate-the-java-io-thread-in-3-min-by-deepflow-tracing/index.html)


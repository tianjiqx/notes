# 并行执行

## volcano xchange


## Morsel-Driven 

多核时代，由于部分 CPU 和部分内存的绑定关系，CPU 访问内存是不均匀（NUMA）的。也即，对于某一个 CPU 核来说，本机上一部分内存访问延迟较低，另一部分内存延迟要高。
传统火山模型，使用 Exchange 算子来进行并发。其他算子并不感知多线程，因此也就没办法就近内存调度计算（硬件亲和性）。也即，非 NUMA-local。
为了解决此问题，论文在数据维度：对数据集进行水平分片，一个 NUMA-node 处理一个数据分片；对每个分片进行垂直分段（Morsel），在 Morsel 粒度上进行并发调度和抢占执行。
在计算维度：为每个 CPU 预分配一个线程，在调度时，每个线程只接受数据块（Morsel）分配到本 NUMA-node 上的任务；当线程间子任务的执行进度不均衡时，快线程会” 窃取 “本应调度到其他线程的任务，从而保证一个 Query 的多个子任务大约同时完成，而不会出现” 长尾 “分片。


## REF

- 风空之岛 blogs
    - [Scheduling-Blog-Overview](http://47.241.45.216/2022/05/29/Scheduling-Blog-Overview/)
    - [Task execution basics in Velox](http://47.241.45.216/2024/06/22/Task-execution-basics-in-Velox/)
    - [SIGMOD'14: Morsel-Driven Parallelism](http://47.241.45.216/2023/11/03/SIGMOD-14-Morsel-Driven-Parallelism/)
    - [Parallel Data Processing with MapReduce: A Survey](http://47.241.45.216/2023/06/14/Parallel-Data-Processing-with-MapReduce-A-Survey/)
    - [Parallel and Distributed Query Processing](http://47.241.45.216/2022/06/05/Parallel-and-Distributed-Query-Processing/)
- [morsel-driven-parallelism-numa-aware-query-evaluation](https://frankma.me/posts/papers/morsel-driven-parallelism-numa-aware-query-evaluation/)
- [NUMA-Aware 执行引擎论文解读](https://www.qtmuniao.com/2023/08/21/numa-aware-execution-engine/)
- [PolarDB-X 并行计算框架](https://zhuanlan.zhihu.com/p/346320114)
- [新硬件时代的并行框架：Morsel-Driven Parallelism: A NUMA-Aware Query Evaluation Framework for the Many-Core Age](https://zhuanlan.zhihu.com/p/615029386)
- [volcano执行引擎论文阅读：Volcano-An Extensible and Parallel Query Evaluation System](https://zhuanlan.zhihu.com/p/649145153)
- [【数据库内核】物理计算引擎 Push 模型之编译执行_数据库 push pull 模型](https://blog.csdn.net/Night_ZW/article/details/108359927)

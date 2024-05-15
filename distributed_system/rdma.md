
# RDMA

RDMA(remote direct memory access)即远端直接内存访问，是一种高性能网络通信技术，具有高带宽、低延迟、无CPU消耗、零拷贝等优点。相比kernel TCP、DPDK等传统通信手段，RDMA在延迟、吞吐和CPU消耗方面均有明显优势。

场景： 
- 数据库 hash join 交换数据
- 日志传输,副本同步


缺点：
- 专有的RNIC 网卡，成本


## REF

- [一个极简的RDMA hello world程序](https://zhuanlan.zhihu.com/p/654739175)
- [阿里RDMA通信库X-RDMA论文精读](https://zhuanlan.zhihu.com/p/673535809)

- [RDMA-远程直接内存访问-00-overview](https://houbb.github.io/2019/11/20/rdma-00-overview)

- [基于 RDMA 的分布式系统研究进展](https://zhuanlan.zhihu.com/p/519986290)

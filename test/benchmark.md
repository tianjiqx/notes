# 数据库基准测试集
[TOC]

## 搜索/日志

### ES esrally

curl -O https://raw.githubusercontent.com/elastic/rally-tracks/master/download.sh
chmod u+x download.sh
./download.sh http_logs
下载完成，可以在  ~/.rally/benchmarks/data/http_logs 目录下找到


### loghub

[logpai/loghub](https://github.com/logpai/loghub)


### openaiops

[log数据](https://www.aiops.cn/log-data/) 一些汇总，基本来源loghub


## 时序

### TSBS 时间系列基准套件

[TSBS](https://github.com/timescale/tsbs) 基于 influxdata/influxdb-comparisons 的时序评测基准


[more](tsbs.md)


### influxdata/influxdb-comparisons


[influxdata/influxdb-comparisons](https://github.com/influxdata/influxdb-comparisons)



## OLAP

### ClickBench

- [ClickBench](https://benchmark.clickhouse.com/)
    - [带你看懂clickbench打榜报告的内容](https://www.cnblogs.com/syw20170419/p/17381314.html) 

### TPC-DS

### SSB


## OLTP

### TPC-C

### sysbench

[sysbench](https://github.com/akopytov/sysbench)


## 其他

### YCSB
Yahoo! Cloud Serving Benchmark，是由雅虎公司开发的一个开源工具，旨在对云服务和数据库系统进行基准性能测试。它主要用于评估和比较不同键值存储系统和云数据库服务的性能表现。YCSB起初设计用于测试NoSQL数据库，但随着时间发展，它的应用范围已扩展到支持多种数据库技术，包括关系型数据库和其他分布式数据存储解决方案。



[benchANT](https://benchant.com/ranking/database-ranking)
- [benchANT/YCSB](https://github.com/benchANT/YCSB)


- [StarRocks 查询优化分析](https://zhuanlan.zhihu.com/p/706527168) TPC-DS/TPCH相关的优化
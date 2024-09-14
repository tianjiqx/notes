# VictoriaMetrics

## Tech

### small 文件合并

某类似系统：
> 对只读的历史数据, 通过 force merge, 将每个分片内多个 segments 合并为单个 segment, 可有效降低存储成本. 目前测试数据表明, 这可以降低指标历史存储成本 20%~40%.

###  Gorilla 编码优化

步骤：
- 按单个时间序列对数据进行分组
- 按时间戳对每个时间序列的（时间戳，值）数据点进行排序。
- 使用增量的增量编码对后续时间戳进行编码。这用较小的偏差值来替代后续数据点之间的间隔的大时间戳。与原始时间戳相比，偏差值用更少的比特数编码。
- 对后续浮点值的二进制表示进行XOR。Gorilla paper clam这通常会给出具有大量前导和尾随零位的二进制值，这些值可以有效地打包成更小数量的位。（被质疑）

Gorilla为典型的时间序列数据提供3x-8x压缩，即它将每个16字节（时间戳，值）数据点压缩为2-5字节。

改进：应用XOR编码之前将浮点值转换为整数，整形的XOR，包含很多前导零，因此它们可以有效地打包成更少数量的位

- 任何浮点数序列都可以通过乘以10^N转换为整数序列，其中N是时间序列中所有值的小数点后的最大位数
- 整形越界，通过除以10^M来规范化整数，其中M是允许将所有时间序列值拟合到64位并删除常见尾随十进制零的最小值。


## 部署
docker pull victoriametrics/victoria-metrics:latest
docker run -it --rm -v `pwd`/victoria-metrics-data:/victoria-metrics-data -p 8428:8428 victoriametrics/victoria-metrics:latest




## TSBS 测试

```shell
# 注意 retentionPeriod配置，超过时间的数据写入后会丢弃
./tsbs_generate_data --use-case="devops" --seed=123 --scale=400 \                            
    --timestamp-start="2016-01-01T00:00:00Z" \
    --timestamp-end="2016-01-04T00:00:00Z" \
    --log-interval="10s" --format="victoriametrics" > /home/tianjiqx/newdisk/devops/devops-victoriametrics-data

./tsbs_load_victoriametrics --file /home/tianjiqx/newdisk/devops/devops-victoriametrics-data

Summary:
loaded 1047168000 metrics in 974.477sec with 1 workers (mean rate 1074594.74 metrics/sec)
loaded 93312000 rows in 974.477sec with 1 workers (mean rate 95755.97 rows/sec)



```

data 空间存储大小： 671MB 取得最优，比doris略好
index 空间： 17M


## REF

- [VictoriaMetrics源码：tv的压缩](https://segmentfault.com/a/1190000043749609)
- [浅析下开源时序数据库VictoriaMetrics的存储机制](https://zhuanlan.zhihu.com/p/368912946)
- [时序数据库-06-04-vm VictoriaMetrics storage 存储原理简介](https://houbb.github.io/2019/04/01/database-time-seriers-06-04-vm-storage)

- [WAL的使用在现代时间序列数据库中看起来已经被打破了](https://valyala.medium.com/wal-usage-looks-broken-in-modern-time-series-databases-b62a627ab704)
    - VictoriaMetrics 将传入的数据缓冲在RAM中，并定期将其刷新到磁盘上类似于SSTable的数据结构中。刷新间隔被硬编码为一秒。

- [VictoriaMetrics: achieving better compression than Gorilla for time series data](https://faun.pub/victoriametrics-achieving-better-compression-for-time-series-data-than-gorilla-317bc1f95932): VM 使用的压缩技术

- [blogs: VictoriaMetrics 作者 Aliaksandr Valialkin](https://valyala.medium.com/)

- [Evaluating Performance and Correctness](https://www.robustperception.io/evaluating-performance-and-correctness/):  Prometheus 社区对 VictoriaMetrics PromQL 语义不兼容问题
- [Evaluating Performance and Correctness](https://valyala.medium.com/evaluating-performance-and-correctness-victoriametrics-response-e27315627e87): VictoriaMetrics response
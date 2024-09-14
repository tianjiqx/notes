# VictoriaMetrics



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


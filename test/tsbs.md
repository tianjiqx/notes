


### TSBS 时间系列基准套件

[TSBS](https://github.com/timescale/tsbs) 基于 influxdata/influxdb-comparisons 的时序评测基准

（遗憾，似乎不在维护）


#### 构建
前置：已经安装 go 环境

```
git clone git@github.com:timescale/tsbs.git
cd tsbs
make
```

构建的各执行程序在 tsbs/bin 目录

#### 数据生成

```
./tsbs_generate_data --use-case="devops" --seed=123 --scale=4000 \
    --timestamp-start="2016-01-01T00:00:00Z" \
    --timestamp-end="2016-01-04T00:00:00Z" \
    --log-interval="10s" --format="clickhouse" \
    | gzip > /home/tianjiqx/newdisk/clickhouse-data.gz

--use-case：使用场景，包括iot、devops、cpu-only，例如iot；
--seed：用于确定性生成的 PRNG 种子。例如：123；
--scale：要生成的卡车/设备数量。例如：50000；
--timestamp-start：数据中时间戳的开始时间。例如：2016-01-01T00:00:00Z；
--timestamp-end：数据中时间戳的结束时间。例如：2016-01-01T00:10:00Z；
--log-interval：每个设备的每次读取之间应该间隔多长时间，以秒为单位。例如：10s；
--format：需要生成的数据库，例如: clickhouse。

```


#### devops 数据集说明

tags(10):

hostname=host_0,region=eu-west-1,datacenter=eu-west-1c,rack=87,os=Ubuntu16.04LTS,arch=x64,team=NYC,service=18,service_version=1,service_environment=production

metrics(9):
cpu,usage_user,usage_system,usage_idle,usage_nice,usage_iowait,usage_irq,usage_softirq,usage_steal,usage_guest,usage_guest_nice
disk,total,free,used,used_percent,inodes_total,inodes_free,inodes_used
diskio,reads,writes,read_bytes,write_bytes,read_time,write_time,io_time
kernel,boot_time,interrupts,context_switches,processes_forked,disk_pages_in,disk_pages_out
mem,total,available,used,free,cached,buffered,used_percent,available_percent,buffered_percent
net,bytes_sent,bytes_recv,packets_sent,packets_recv,err_in,err_out,drop_in,drop_out
nginx,accepts,active,handled,reading,requests,waiting,writing
postgresl,numbackends,xact_commit,xact_rollback,blks_read,blks_hit,tup_returned,tup_fetched,tup_inserted,tup_updated,tup_deleted,conflicts,temp_files,temp_bytes,deadlocks,blk_read_time,blk_write_time
redis,uptime_in_seconds,total_connections_received,expired_keys,evicted_keys,keyspace_hits,keyspace_misses,instantaneous_ops_per_sec,instantaneous_input_kbps,instantaneous_output_kbps,connected_clients,used_memory,used_memory_rss,used_memory_peak,used_memory_lua,rdb_changes_since_last_save,sync_full,sync_partial_ok,sync_partial_err,pubsub_channels,pubsub_patterns,latest_fork_usec,connected_slaves,master_repl_offset,repl_backlog_active,repl_backlog_size,repl_backlog_histlen,mem_fragmentation_ratio,used_cpu_sys,used_cpu_user,used_cpu_sys_children,used_cpu_user_children


--scale=400

400 * 3 * 24 * 60 * 6 * 9 = 9331 2000 行数据


单设备一天 24 * 60 * 6 = 8640


cpu-only 是devops中cpu的数据

#### iot

tags(8)：

name string,fleet string,driver string,model string,device_version string,load_capacity float32,fuel_capacity float32,nominal_fuel_consumption float32

指标(2)：
diagnostics,fuel_state,current_load,status
readings,latitude,longitude,elevation,velocity,heading,grade,fuel_consumption


[可选] gzip 压缩生成结果  

#### 数据导入

```shell
./tsbs_load_clickhouse --db-name benchmark  --file ~/newdisk/iot-clickhouse-data 

# 其他参数， --help 查看

```



注意官方 clickhouse 建表语句陈旧，需要修改

#### 查询语句

```
# 查看存储空间

SELECT name,total_bytes,total_rows FROM system.tables WHERE database = 'benchmark'

# 生成10条查询语句 
./tsbs_generate_queries --use-case="devops" --db-name=benchmark  --seed=123 --scale=400 \
--timestamp-start="2016-01-01T00:00:00Z" \
--timestamp-end="2016-01-04T00:00:01Z" \
--queries=10 --query-type="single-groupby-1-1-1" --format="clickhouse" \
--file=/home/tianjiqx/newdisk/clickhouse-single-groupby-1-1-1


# 执行
./tsbs_run_queries_clickhouse --db-name=benchmark --file=/home/tianjiqx/newdisk/clickhouse-single-groupby-1-1-1 \
--workers=1 --max-queries=10 --results-file=/home/tianjiqx/newdisk/clickhouse-single-groupby-1-1-1.result


```


## 测试

环境：

AMD® Ryzen 7 7840hs w/ radeon 780m graphics × 16
16*2 G 内存 ddr5  5600MT/s
1T SSD  7000 MB/s
time dd if=/dev/zero of=/home/tianjiqx/test.txt bs=4k count=200000
819200000字节（819 MB，781 MiB）已复制，0.699636 s，1.2 GB/s

time dd if=/dev/zero of=/home/tianjiqx/test.txt bs=4k count=200000 oflag=direct
819200000字节（819 MB，781 MiB）已复制，2.41827 s，339 MB/s


--scale=400

原始数据集大小 9331 2000 行
ck： 类csv   25G
ketadb： json 55G



| 系统         | size（GB）   | load time（s） | 压缩比 | 速度（row/s） |
| ---------- | ---------- | ------------ | --- | --------- |
| clickhouse | 2.66       | 659.041      |     | 141,596   |
| doris      | 741.278 MB | 82.449       |     | 1,132,427 |
| clickhouse_tsv | 3.02       | 659.041      |     | 141,596   |
| doris_tsv      | 768.334 MB | 126.646      |     | 1,308,631 |


导入时间，各个系统导入方式不同，参考意义不大
clickhouse 使用9 + 1 总共10张表存储数据

注意：
- tag id 生成在测试中基于内存map, 真实场景应该如何扩展生成tag id？（tagkv的 hashcode？） 
- tags 长度 对于devops 是固定的
- 并且按照 tag_id, created_at 有序


clickhouse: 单线程导入，查询时使用 in 查询从 tags 表进行查询
doirs: 单线程，导入 clickhouse 导出的 csv文件
clickhouse_tsv: tsv导入, tag未分离，并且保留tag_id 保证有序
doris_tsv  类似 clickhouse_tsv


问题：
- 每类指标系列，需要使用单独的表，成千上万的表，是否元信息会有问题？
- 指标的tag的更新，tag字段的增减，对应schema变更问题
    - doris [variant](https://doris.apache.org/zh-CN/docs/sql-manual/sql-types/Data-Types/VARIANT?_highlight=v#variant) 类型 ?


```
SELECT
    toStartOfMinute(created_at) AS minute,
    max(usage_user) AS max_usage_user
FROM cpu
WHERE tags_id IN (SELECT id FROM tags WHERE hostname IN ('host_311')) AND (created_at >= '2016-01-02 11:06:44') AND (created_at < '2016-01-02 12:06:44')
GROUP BY minute
ORDER BY minute ASC
```


| query                 | 说明                                              | clickhouse  <br>(avg) ms | doris |
| --------------------- | ----------------------------------------------- | ------------------------ | ----- |
| single-groupby-1-1-1  | 对 1 个主机的一个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时       | 11.40,9.02               | 27.46 |
| single-groupby-1-1-12 | 1 台主机的一个指标上的简单聚合 （MAX），每 5 分钟一次，持续 12 小时        | 6.16                     | 16.71 |
| single-groupby-1-8-1  | 对 8 个主机的一个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时       | 6.24                     | 14.79 |
| single-groupby-5-1-1  | 对 1 台主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时     | 6.20                     | 13.89 |
| single-groupby-5-1-12 | 对 1 台主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 12 小时    | 6.29                     | 13.98 |
| single-groupby-5-8-1  | 对 8 个主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时     | 6.05                     | 13.92 |
| cpu-max-all-1         | 聚合单个主机 1 小时内每小时的所有 CPU 指标                       | 6.33                     | 11.80 |
| cpu-max-all-8         | 在 1 小时内聚合 8 台主机每小时的所有 CPU 指标                    | 6.14                     | 14.45 |
| double-groupby-1      | 跨时间和主机进行聚合，在 24 小时内平均每个主机每小时 1 个 CPU 指标         | 5.36                     | 12.29 |
| double-groupby-5      | 跨时间和主机进行聚合，在 24 小时内平均每个主机每小时提供 5 个 CPU 指标       | 4.58                     | 13.92 |
| double-groupby-all    | 跨时间和主机进行聚合，给出每个主机每小时 24 小时内所有 （10） 个 CPU 指标的平均值 | 4.76                     | 11.47 |
| high-cpu-all          | 一个指标高于所有主机阈值的所有读数                               | 4.73                     | 11.93 |
| high-cpu-1            | 一个指标高于特定主机阈值的所有读数                               | 4.76                     | 12.79 |
| lastpoint             | 每个主机的最后读数                                       | 5.02                     | 11.82 |
| groupby-orderby-limit | 随机选择的终点之前的最后 5 个汇总读数（跨时间）                       | 4.72                     | 11.67 |


（每 5 分钟一次？ 检查语句似乎是每分钟）


#### REF

- [一文走进时序数据库性能测试工具 TSBS](https://zhuanlan.zhihu.com/p/649214414)
- [TSBS 是什么？为什么时序数据库 TDengine 会选择它作为性能对比测试平台?](https://zhuanlan.zhihu.com/p/610366672)

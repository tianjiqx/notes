


### TSBS 时间系列基准套件

[TSBS](https://github.com/timescale/tsbs) 基于 influxdata/influxdb-comparisons 的时序评测基准


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

```
--use-case：使用场景，包括iot、devops、cpu-only，例如iot；
--seed：用于确定性生成的 PRNG 种子。例如：123；
--scale：要生成的卡车/设备数量。例如：50000；
--timestamp-start：数据中时间戳的开始时间。例如：2016-01-01T00:00:00Z；
--timestamp-end：数据中时间戳的结束时间。例如：2016-01-01T00:10:00Z；
--log-interval：每个设备的每次读取之间应该间隔多长时间，以秒为单位。例如：10s；
--format：需要生成的数据库，例如: clickhouse。


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



#### REF

- [一文走进时序数据库性能测试工具 TSBS](https://zhuanlan.zhihu.com/p/649214414)
- [TSBS 是什么？为什么时序数据库 TDengine 会选择它作为性能对比测试平台?](https://zhuanlan.zhihu.com/p/610366672)


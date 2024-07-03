


### TSBS 时间系列基准套件

[TSBS](https://github.com/timescale/tsbs) 基于 influxdata/influxdb-comparisons 的时序评测基准

（遗憾，似乎不在维护）


#### 构建
前置：已经安装 go 环境
`
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

### 环境

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

#### load & storage
| 系统         | size（GB）   | load time（s） | 压缩比 | 速度（row/s） |
| ---------- | ---------- | ------------ | --- | --------- |
| clickhouse | 2.95       | 659.041      |  4.0   | 141,596   |
| doris      | 741.278 MB | 82.449       |  1.0   | 1,132,427 |
| clickhouse_tsv | 3.02       | 659.041      | 4.1    | 1,308,631   |
|clickhouse+codec |	2.73 |	2673.98	| 3.7 |	34,896 |
|clickhouse+codec+tsv |	2.835 |	1095.85 |	3.8 |	85,150 |
| doris_tsv      | 768.334 MB | 126.646 | 1.02    | 736,793 |
| doris_varint +倒排索引      | 821.751 MB | 229.866      |  1.09   | 405,940 |
| ES（6.8）     | 10.8 | 1980      |  14.67   | 47,127 |


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
doris_varint + 倒排索引，使用 variant 存储tag字段，并对 tags 字段构建倒排索引


clickhouse+codec 使用 DoubleDelta + Gorilla 编码

doris 默认数据压缩方式  lz4， 60K
be/src/exec/decompressor.cpp 


clichouse 默认列压缩方式 lz4， 压缩块大小，最小  min_compress_block_size 65,536=64k， 
但是受 index_granularity（默认8192） 影响，可能一个块大小会超过 64K。

[clickhouse columns compression codec](https://clickhouse.com/docs/en/sql-reference/statements/create/table#column_compression_codec) 
  - 支持对double类型 Gorilla 编码 Gorilla(bytes_size)，bytes_size values: 1, 2, 4, 8
    - slow_values Float32 CODEC(Gorilla)  
  - DoubleDelta
    - timestamp DateTime CODEC(DoubleDelta)

  - 其他 lz4, zstd 等 

问题：
- 每类指标系列，需要使用单独的表，成千上万的表，是否元信息会有问题？
- 指标的tag的更新，tag字段的增减，对应schema变更问题
    - doris [variant](https://doris.apache.org/zh-CN/docs/sql-manual/sql-types/Data-Types/VARIANT?_highlight=v#variant) 类型 ? 将写入的 JSON 列存化，使用 variant 存储tag字段
    - [variant](https://doris.apache.org/docs/sql-manual/sql-types/Data-Types/VARIANT/) 注意：不能直接作为key排序，分组key, 过滤支持，需要类似 `cast(cpu.tags['hostname'] as text) as hostname` 函数转换后使用 
    - variant ，ui即倒排索引 会对增加少量存储空间，但依然维持了非常好的压缩比例


#### query

single-groupby-1-1-1
```
SELECT
    toStartOfMinute(created_at) AS minute,
    max(usage_user) AS max_usage_user
FROM cpu
WHERE tags_id IN (SELECT id FROM tags WHERE hostname IN ('host_311')) AND (created_at >= '2016-01-02 11:06:44') AND (created_at < '2016-01-02 12:06:44')
GROUP BY minute
ORDER BY minute ASC
```

其他，可以查看 fork的 tsbs 仓库

| query                 | 说明                                              | clickhouse  <br>(avg) ms | doris | doris_varint |
| --------------------- | ----------------------------------------------- | ------------------------ | ----- | ------------ |
| single-groupby-1-1-1  | 对 1 个主机的一个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时       | 7.87                     | 22.55 | 22.97        |
| single-groupby-1-1-12 | 1 台主机的一个指标上的简单聚合 （MAX），每 5 分钟一次，持续 12 小时        | 5.83                     | 19.17 | 18.39        |
| single-groupby-1-8-1  | 对 8 个主机的一个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时       | 8.03                     | 19.75 | 14.25        |
| single-groupby-5-1-1  | 对 1 台主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时     | 11.50                    | 19.74 | 16.13        |
| single-groupby-5-1-12 | 对 1 台主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 12 小时    | 7.20                     | 20.24 | 15.80        |
| single-groupby-5-8-1  | 对 8 个主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时     | 13.83                    | 18.60 | 14.78        |
| cpu-max-all-1         | 聚合单个主机 1 小时内每小时的所有 CPU 指标                       | 15.07                    | 15.48 | 16.08        |
| cpu-max-all-8         | 在 1 小时内聚合 8 台主机每小时的所有 CPU 指标                    | 26.60                    | 17.18 | 19.35        |
| double-groupby-1      | 跨时间和主机进行聚合，在 24 小时内平均每个主机每小时 1 个 CPU 指标         | 13.30                    | 32.51 | 38.60        |
| double-groupby-5      | 跨时间和主机进行聚合，在 24 小时内平均每个主机每小时提供 5 个 CPU 指标       | 32.16                    | 40.65 | 50.33        |
| double-groupby-all    | 跨时间和主机进行聚合，给出每个主机每小时 24 小时内所有 （10） 个 CPU 指标的平均值 | 58.06                    | 55.51 | 68.82        |
| high-cpu-all          | 一个指标高于所有主机阈值的所有读数                               | 122.87                   | 74.76 | 90.04        |
| high-cpu-1            | 一个指标高于特定主机阈值的所有读数                               | 5.11                     | 8.16  | 11.53        |
| lastpoint             | 每个主机的最后读数                                       | 32.34                    | 48.73 | 55.30        |
| groupby-orderby-limit | 随机选择的终点之前的最后 5 个汇总读数（跨时间）                       | 10.63                    | 24.14 | 29.24        |


（每 5 分钟一次？ 检查语句似乎是每分钟）


clickhouse 相比 doris 在指标查询上，一般都快一倍，不过似乎在更大数据量的case上，doris 反而变相更良好，例如 high-cpu-all， cpu-max-all-8，double-groupby-all。
过滤效率的差异？ clickhouse 索引空间换来的查询性能？

varint 对于过滤影响不大，主要参与分组聚合、排序字段时，cast函数带来了额外开销，导致查询耗时增加。


### QPS 测试

q1: doris-single-groupby-1-1-1
对 1 个主机的一个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时

```
SELECT
                   DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:00') AS minute,
        max(usage_user) AS max_usage_user
    FROM cpu
    WHERE tags_id IN (SELECT id FROM tags WHERE hostname IN ('host_${__Random(0,399,)}')) AND (created_at >= '2016-01-03 21:17:20') AND (created_at < '2016-01-03 22:17:20')
    GROUP BY minute
    ORDER BY minute ASC
```

| 样本数           | 均值ms | 吞吐量   |
| ------------- | ---- | ----- |
| 10*500=10000  | 13   | 685.7 |
| 25*400=10000  | 31   | 740.6 |
| 50*200=10000  | 64   | 723.4 |
| 100*100=10000 | 135  | 691.9 |


clickhouse

```
SELECT
    toStartOfMinute(created_at) AS minute,
    max(usage_user) AS max_usage_user
FROM cpu
WHERE tags_id IN (SELECT id FROM tags WHERE hostname IN ('host_${__Random(0,399,)}')) AND (created_at >= '2016-01-03 21:17:20') AND (created_at < '2016-01-03 22:17:20')
GROUP BY minute
ORDER BY minute ASC
```

| 样本数           | 均值ms | 吞吐量   |
| ------------- | ---- | ----- |
| 10*500=10000  | 12   | 749.3 |
| 25*400=10000  | 27   | 842.1 |
| 50*200=10000  | 54   | 851.1 |
| 100*100=10000 | 106  | 861   |

qps 吞吐也基本一直，clickhouse 吞吐略好


#### clickhouse 存储分析


clickhouse+codec+tsv：

建表

```sql
CREATE TABLE cpu
(
    `created_date` Date DEFAULT today() CODEC(DoubleDelta),
    `created_at` DateTime DEFAULT now() CODEC(DoubleDelta),
    `time` String,
    `tags_id` UInt32,
    `usage_user` Nullable(Float64) CODEC(Gorilla),
    `usage_system` Nullable(Float64) CODEC(Gorilla),
    `usage_idle` Nullable(Float64) CODEC(Gorilla),
    `usage_nice` Nullable(Float64) CODEC(Gorilla),
    `usage_iowait` Nullable(Float64) CODEC(Gorilla),
    `usage_irq` Nullable(Float64) CODEC(Gorilla),
    `usage_softirq` Nullable(Float64) CODEC(Gorilla),
    `usage_steal` Nullable(Float64) CODEC(Gorilla),
    `usage_guest` Nullable(Float64) CODEC(Gorilla),
    `usage_guest_nice` Nullable(Float64) CODEC(Gorilla),
    `additional_tags` String DEFAULT ''
)
    ENGINE = MergeTree
PARTITION BY created_date
PRIMARY KEY (tags_id, created_at)
ORDER BY (tags_id, created_at)
SETTINGS index_granularity = 8192;
```



```
// table
cpu	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/
disk	/var/lib/clickhouse/store/86a/86ad63c0-8270-4f57-8488-ad6bdfbc2dbf/
diskio	/var/lib/clickhouse/store/a6d/a6dc1a81-188d-4b03-95c5-1f1bf7c918c2/
kernel	/var/lib/clickhouse/store/4be/4be82320-37fe-4ff4-913e-49310c6dec97/
mem	/var/lib/clickhouse/store/13a/13af2f47-6046-496d-9691-6c14fc8f4db4/
net	/var/lib/clickhouse/store/e95/e9583b2e-b7b7-42f8-ab7e-ab0c7e32ccf4/
nginx	/var/lib/clickhouse/store/679/679392b5-f607-4a3d-a4e6-324635bfd6b0/
postgresl	/var/lib/clickhouse/store/0f4/0f482d6d-d307-4ae2-ba21-549c0016bd39/
redis	/var/lib/clickhouse/store/bba/bba7ba31-02ec-48b2-8733-27c7709f5c81/
tags	/var/lib/clickhouse/store/8d1/8d1966e0-0248-4c6d-ac3f-eb2e9c1a6820/

231M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/
181M	/var/lib/clickhouse/store/86a/86ad63c0-8270-4f57-8488-ad6bdfbc2dbf/
291M	/var/lib/clickhouse/store/a6d/a6dc1a81-188d-4b03-95c5-1f1bf7c918c2/
219M	/var/lib/clickhouse/store/4be/4be82320-37fe-4ff4-913e-49310c6dec97/
566M	/var/lib/clickhouse/store/13a/13af2f47-6046-496d-9691-6c14fc8f4db4/
317M	/var/lib/clickhouse/store/e95/e9583b2e-b7b7-42f8-ab7e-ab0c7e32ccf4/
191M	/var/lib/clickhouse/store/679/679392b5-f607-4a3d-a4e6-324635bfd6b0/
265M	/var/lib/clickhouse/store/0f4/0f482d6d-d307-4ae2-ba21-549c0016bd39/
678M	/var/lib/clickhouse/store/bba/bba7ba31-02ec-48b2-8733-27c7709f5c81/
84K	/var/lib/clickhouse/store/8d1/8d1966e0-0248-4c6d-ac3f-eb2e9c1a6820/


cpu：

total 231M

34M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160101_2_21_1
5.2M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160101_25_25_0
5.2M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160101_29_29_0
7.5M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160101_33_33_0
736K	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160101_36_36_0
44M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160102_1_24_1
8.4M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160102_28_28_0
12M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160102_31_31_0
14M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160102_32_32_0
608K	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160102_35_35_0
9.2M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160103_26_26_0
9.1M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160103_30_30_0
54M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160103_3_22_1
5.3M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160103_34_34_0
2.7M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160104_27_27_0
24M	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/20160104_4_23_1
4.0K	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/detached
4.0K	/var/lib/clickhouse/store/40c/40ccfd57-21e2-47fe-8f34-a0ca636357e6/format_version.txt

20160101_2_21_1:
total： 34M

7.3M	time.bin
1.5M	usage_user.null.bin
1.5M	usage_system.null.bin
1.5M	usage_steal.null.bin
1.5M	usage_softirq.null.bin
1.5M	usage_nice.null.bin
1.5M	usage_irq.null.bin
1.5M	usage_iowait.null.bin
1.5M	usage_idle.null.bin
1.5M	usage_guest.null.bin
1.5M	usage_guest_nice.null.bin
1.2M	usage_user.bin
1.2M	usage_system.bin
1.2M	usage_steal.bin
1.2M	usage_softirq.bin
1.2M	usage_nice.bin
1.2M	usage_irq.bin
1.2M	usage_iowait.bin
1.2M	usage_idle.bin
1.2M	usage_guest_nice.bin
1.2M	usage_guest.bin

4.0K	usage_user.null.cmrk2
4.0K	usage_user.cmrk2
4.0K	usage_system.null.cmrk2
4.0K	usage_system.cmrk2
...

4.0K	count.txt
4.0K	columns.txt
4.0K	checksums.txt

192K	created_at.bin
4.0K	created_at.cmrk2
188K	created_date.bin
4.0K	created_date.cmrk2
4.0K	minmax_created_date.idx


```

40ccfd57-21e2-47fe-8f34-a0ca636357e6：

```
find . -type f -exec du -a {} + | awk -F'/' '{print $1 $NF}' | awk '{sum[$2] += $1} END {for (key in sum) print sum[key], key}' | sort -nr 

单位 K， total: 236440 K

50080 .time.bin
10104 .usage_user.null.bin
10104 .usage_system.null.bin
10104 .usage_steal.null.bin
10104 .usage_softirq.null.bin
10104 .usage_nice.null.bin
10104 .usage_irq.null.bin
10104 .usage_iowait.null.bin
10104 .usage_idle.null.bin
10104 .usage_guest.null.bin
10104 .usage_guest_nice.null.bin
7956 .usage_user.bin
7920 .usage_steal.bin
7912 .usage_irq.bin
7912 .usage_idle.bin
7900 .usage_guest_nice.bin
7896 .usage_nice.bin
7892 .usage_system.bin
7884 .usage_softirq.bin
7880 .usage_guest.bin
7872 .usage_iowait.bin
1340 .created_at.bin
1300 .created_date.bin
1256 .data.bin
228 .tags_id.bin
64 .serialization.json
64 .primary.cidx
64 .partition.dat
64 .minmax_created_date.idx
64 .metadata_version.txt
64 .default_compression_codec.txt
64 .count.txt
64 .columns.txt
64 .checksums.txt
56 .usage_user.null.cmrk2
56 .usage_user.cmrk2
56 .usage_system.null.cmrk2
56 .usage_system.cmrk2
56 .usage_steal.null.cmrk2
56 .usage_steal.cmrk2
56 .usage_softirq.null.cmrk2
56 .usage_softirq.cmrk2
56 .usage_nice.null.cmrk2
56 .usage_nice.cmrk2
56 .usage_irq.null.cmrk2
56 .usage_irq.cmrk2
56 .usage_iowait.null.cmrk2
56 .usage_iowait.cmrk2
56 .usage_idle.null.cmrk2
56 .usage_idle.cmrk2
56 .usage_guest.null.cmrk2
56 .usage_guest_nice.null.cmrk2
56 .usage_guest_nice.cmrk2
56 .usage_guest.cmrk2
56 .time.cmrk2
56 .tags_id.cmrk2
56 .created_date.cmrk2
56 .created_at.cmrk2
56 .additional_tags.sparse.idx.cmrk2
56 .additional_tags.sparse.idx.bin
56 .additional_tags.cmrk2
8 .data.cmrk3
4 .format_version.txt
0 .additional_tags.bin

占比

0.211808 .time.bin
0.0427339 .usage_user.null.bin
0.0427339 .usage_system.null.bin
0.0427339 .usage_steal.null.bin
0.0427339 .usage_softirq.null.bin
0.0427339 .usage_nice.null.bin
0.0427339 .usage_irq.null.bin
0.0427339 .usage_iowait.null.bin
0.0427339 .usage_idle.null.bin
0.0427339 .usage_guest.null.bin
0.0427339 .usage_guest_nice.null.bin
0.0336491 .usage_user.bin
0.0334969 .usage_steal.bin
0.033463 .usage_irq.bin
0.033463 .usage_idle.bin
0.0334123 .usage_guest_nice.bin
0.0333954 .usage_nice.bin
0.0333784 .usage_system.bin
0.0333446 .usage_softirq.bin
0.0333277 .usage_guest.bin
0.0332939 .usage_iowait.bin
0.0056674 .created_at.bin
0.00549822 .created_date.bin
0.00531213 .data.bin
0.000964304 .tags_id.bin
0.000270682 .serialization.json
0.000270682 .primary.cidx
0.000270682 .partition.dat
0.000270682 .minmax_created_date.idx
0.000270682 .metadata_version.txt
0.000270682 .default_compression_codec.txt
0.000270682 .count.txt
0.000270682 .columns.txt


 ```


clickhouse_tsv

默认lz4

```
cpu	/var/lib/clickhouse/store/88c/88ca94d8-2af6-45ce-a7bb-2bf7680f42b3/
disk	/var/lib/clickhouse/store/607/607f0c20-6ba7-4a6c-839b-0efff681d268/
diskio	/var/lib/clickhouse/store/b86/b86ee960-771a-43f3-9324-deea485be34a/
kernel	/var/lib/clickhouse/store/32c/32c952fb-2156-4e10-bade-0729f7da2240/
mem	/var/lib/clickhouse/store/758/7580b925-df2a-4a76-9fc5-4bf59f73fad2/
net	/var/lib/clickhouse/store/0cf/0cfca57d-e332-4e59-b703-24859426685a/
nginx	/var/lib/clickhouse/store/5da/5dac7a4d-d5f0-4a75-ab85-218fcbdea172/
postgresl	/var/lib/clickhouse/store/9b3/9b3adc3d-bc34-4d33-8c7f-d4a81b77ca21/
redis	/var/lib/clickhouse/store/595/59599b1c-247d-43b9-aab6-a40790a141c1/
tags	/var/lib/clickhouse/store/50a/50aeaf7c-4ff9-4f9f-9e96-3298a6df1d4a/

285M	/var/lib/clickhouse/store/88c/88ca94d8-2af6-45ce-a7bb-2bf7680f42b3/
157M	/var/lib/clickhouse/store/607/607f0c20-6ba7-4a6c-839b-0efff681d268/
367M	/var/lib/clickhouse/store/b86/b86ee960-771a-43f3-9324-deea485be34a/
281M	/var/lib/clickhouse/store/32c/32c952fb-2156-4e10-bade-0729f7da2240/
619M	/var/lib/clickhouse/store/758/7580b925-df2a-4a76-9fc5-4bf59f73fad2/
406M	/var/lib/clickhouse/store/0cf/0cfca57d-e332-4e59-b703-24859426685a/
204M	/var/lib/clickhouse/store/5da/5dac7a4d-d5f0-4a75-ab85-218fcbdea172/
125M	/var/lib/clickhouse/store/9b3/9b3adc3d-bc34-4d33-8c7f-d4a81b77ca21/
602M	/var/lib/clickhouse/store/595/59599b1c-247d-43b9-aab6-a40790a141c1/
84K	/var/lib/clickhouse/store/50a/50aeaf7c-4ff9-4f9f-9e96-3298a6df1d4a/


cpu:

total: 285M

63M	20160101_1_2073_23
60K	20160101_2074_2074_0
96M	20160102_2075_5185_23
96M	20160103_5186_8296_23
29M	20160104_8297_9241_22
2.5M	20160104_9242_9333_17
4.0K	detached
4.0K	format_version.txt


20160101_1_2073_23:

12M	time.bin
4.9M	usage_user.bin
4.9M	usage_system.bin
4.9M	usage_steal.bin
4.9M	usage_softirq.bin
4.9M	usage_nice.bin
4.9M	usage_irq.bin
4.9M	usage_iowait.bin
4.9M	usage_idle.bin
4.9M	usage_guest_nice.bin
4.9M	usage_guest.bin
2.2M	created_at.bin


```


```

total: 291596 K

51876 .time.bin
22532 .usage_guest_nice.bin
22528 .usage_idle.bin
22524 .usage_iowait.bin
22524 .usage_guest.bin
22520 .usage_user.bin
22516 .usage_steal.bin
22512 .usage_nice.bin
22512 .usage_irq.bin
22508 .usage_system.bin
22500 .usage_softirq.bin
12528 .created_at.bin
196 .tags_id.bin
100 .created_date.bin
56 .usage_user.null.bin
56 .usage_system.null.bin
56 .usage_steal.null.bin
56 .usage_softirq.null.bin
56 .usage_nice.null.bin
56 .usage_irq.null.bin
56 .usage_iowait.null.bin
56 .usage_idle.null.bin
56 .usage_guest.null.bin
56 .usage_guest_nice.null.bin
24 .serialization.json
24 .primary.cidx
24 .partition.dat
24 .minmax_created_date.idx
24 .metadata_version.txt
24 .default_compression_codec.txt
24 .count.txt
24 .columns.txt
24 .checksums.txt
20 .usage_user.null.cmrk2
20 .usage_user.cmrk2
20 .usage_system.null.cmrk2
20 .usage_system.cmrk2
20 .usage_steal.null.cmrk2
20 .usage_steal.cmrk2
20 .usage_softirq.null.cmrk2
20 .usage_softirq.cmrk2
20 .usage_nice.null.cmrk2
20 .usage_nice.cmrk2
20 .usage_irq.null.cmrk2
20 .usage_irq.cmrk2
20 .usage_iowait.null.cmrk2
20 .usage_iowait.cmrk2
20 .usage_idle.null.cmrk2
20 .usage_idle.cmrk2
20 .usage_guest.null.cmrk2
20 .usage_guest_nice.null.cmrk2
20 .usage_guest_nice.cmrk2
20 .usage_guest.cmrk2
20 .time.cmrk2
20 .tags_id.cmrk2
20 .created_date.cmrk2
20 .created_at.cmrk2
20 .additional_tags.sparse.idx.cmrk2
20 .additional_tags.sparse.idx.bin
20 .additional_tags.cmrk2
16 .data.bin
4 .format_version.txt
4 .data.cmrk3
0 .additional_tags.bin


占比：
0.177904 .time.bin
0.0772713 .usage_guest_nice.bin
0.0772576 .usage_idle.bin
0.0772439 .usage_iowait.bin
0.0772439 .usage_guest.bin
0.0772301 .usage_user.bin
0.0772164 .usage_steal.bin
0.0772027 .usage_nice.bin
0.0772027 .usage_irq.bin
0.077189 .usage_system.bin
0.0771616 .usage_softirq.bin
0.0429636 .created_at.bin
0.000672163 .tags_id.bin
0.00034294 .created_date.bin
0.000192047 .usage_user.null.bin
0.000192047 .usage_system.null.bin
0.000192047 .usage_steal.null.bin
0.000192047 .usage_softirq.null.bin
0.000192047 .usage_nice.null.bin
0.000192047 .usage_irq.null.bin
0.000192047 .usage_iowait.null.bin
0.000192047 .usage_idle.null.bin
0.000192047 .usage_guest.null.bin
0.000192047 .usage_guest_nice.null.bin
...


```


###### 时间类型对比：

DoubleDelta：

1340 .created_at.bin
1300 .created_date.bin

lz4：
12528 .created_at.bin
100 .created_date.bin

对于 时间戳类型DoubleDelta更有优势 (9.35X) ，created_date 日期类型 lz4 压缩更好  

##### double 类型

Gorilla:

7956 .usage_user.bin
7892 .usage_system.bin
7920 .usage_steal.bin

10104 .usage_user.null.bin
10104 .usage_system.null.bin
10104 .usage_steal.null.bin

lz4:

22520 .usage_user.bin
22508 .usage_system.bin
22516 .usage_steal.bin

56 .usage_user.null.bin
56 .usage_system.null.bin
56 .usage_steal.null.bin

usage_user:  22520 + 56 = 22576 KB

10字段 大约 

lz4 空间消耗是 Gorilla 1.25X, Gorilla null文件为什么开销大？



理论数据计算：

cpu 单表 10368000 行，Float64 8B， 10 fields

10368000 * 8B * 10 = 791 MB


lz4 约等于 220 MB

Gorilla 约等于 176 MB


调优： 
- Date DEFAULT today()
- Float64 CODEC(Gorilla)




#### REF

- [一文走进时序数据库性能测试工具 TSBS](https://zhuanlan.zhihu.com/p/649214414)
- [TSBS 是什么？为什么时序数据库 TDengine 会选择它作为性能对比测试平台?](https://zhuanlan.zhihu.com/p/610366672)


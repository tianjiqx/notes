# TSBS 时间系列基准套件

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


# TSV 格式导入
clickhouse-client --time --query "INSERT INTO benchmark.cpu FORMAT TSV" < /home/tianjiqx/newdisk/devops/devops-cpu


```


注意官方 clickhouse 建表语句陈旧，需要修改，可参考 fork的tsbs 仓库。

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

时间序列基数：1200


#### load & storage


| 系统                                               | size（GB）     | load time（s） | 压缩比 | 速度（row/s） |
|----------------------------------------------------|--------------|--------------|--------|-------------|
| clickhouse                                         | 2.95         | 659.041      | 4.0    | 141,596     |
| doris                                              | 741.278 MB   | 82.449       | 1.0    | 1,132,427   |
| clickhouse_tsv                                     | 3.02         | 71.305       | 4.1    | 1,308,631   |
| clickhouse+codec                                   | 2.73         | 2673.98      | 3.7    | 34,896      |
| clickhouse+codec+tsv                               | 2.835        | 1095.85      | 3.8    | 85,150      |
| clickhouse+codec+tsv 优化                          | 1.85         | 460.591      | 2.51   | 202,591     |
| clickhouse+codec+tsv(LZ4HC)                        | 2.42         | 351.65       | 3.34   | 265,354     |
| clickhouse+codec+tsv(LowCardinality)               | 3.05         | 343.001      | 4.21   | 272,045     |
| clickhouse+codec+tsv(no partition)                 | 2.9          | 342.452      | 4.0    | 272,482     |
| clickhouse+codec+tsv(no partition+gorilla)         | 1.64         | 341.411      | 2.27   | 273,312     |
| clickhouse+codec+tsv(no partition+gorilla+float32) | 1.412        | 324.719      | 1.95   | 273,312     |
| clickhouse+codec+tsv(no partition+float32)         | 2.21         | 315.087      | 3.06   | 273,312     |
| doris_tsv                                          | 768.334 MB   | 126.646      | 1.02   | 736,793     |
| doris_varint +倒排索引                             | 821.751 MB   | 229.866      | 1.09   | 405,940     |
| ES（6.8）                                            | 10.8         | 1980         | 14.67  | 47,127      |
| VictoriaMetrics（1.103.0）                         | 671M(data) + 17M(index)=688M | 974.477      | 0.93   | 95,756      |


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

doris 默认数据压缩方式  lz4， 64K (LZ4F_default=LZ4F_max64KB=1 << 16)
be/src/exec/decompressor.cpp 


clickhouse+codec+tsv(LowCardinality) ： 时间 DoubleDelta 编码 + LowCardinality（float64）

clickhouse+codec+tsv(no partition) : 时间 DoubleDelta 编码，lz4， 非分区

clickhouse+codec+tsv(no partition+gorilla) 时间 DoubleDelta + float64 Gorilla + lz4 + 非分区


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

| query                 | 说明                                                                              | clickhouse  <br>(avg) ms | doris | doris_varint | VictoriaMetrics    |
| --------------------- | --------------------------------------------------------------------------------- | ------------------------ | ----- | ------------ | --- |
| single-groupby-1-1-1  | 对 1 个主机的一个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时             | 7.87                     | 22.55 | 22.97        | 1.57    |
| single-groupby-1-1-12 | 1 台主机的一个指标上的简单聚合 （MAX），每 5 分钟一次，持续 12 小时               | 5.83                     | 19.17 | 18.39        |  0.86   |
| single-groupby-1-8-1  | 对 8 个主机的一个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时             | 8.03                     | 19.75 | 14.25        |  1.92   |
| single-groupby-5-1-1  | 对 1 台主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时            | 11.50                    | 19.74 | 16.13        |  1.53   |
| single-groupby-5-1-12 | 对 1 台主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 12 小时           | 7.20                     | 20.24 | 15.80        |  2.45   |
| single-groupby-5-8-1  | 对 8 个主机的 5 个指标进行简单聚合 （MAX），每 5 分钟一次，持续 1 小时            | 13.83                    | 18.60 | 14.78        |  2.24   |
| cpu-max-all-1         | 聚合单个主机 1 小时内每小时的所有 CPU 指标                                        | 15.07                    | 15.48 | 16.08        |  1.56   |
| cpu-max-all-8         | 在 1 小时内聚合 8 台主机每小时的所有 CPU 指标                                     | 26.60                    | 17.18 | 19.35        |  1.72   |
| double-groupby-1      | 跨时间和主机进行聚合，在 24 小时内平均每个主机每小时 1 个 CPU 指标                | 13.30                    | 32.51 | 38.60        |  6.65   |
| double-groupby-5      | 跨时间和主机进行聚合，在 24 小时内平均每个主机每小时提供 5 个 CPU 指标            | 32.16                    | 40.65 | 50.33        |  25.91   |
| double-groupby-all    | 跨时间和主机进行聚合，给出每个主机每小时 24 小时内所有 （10） 个 CPU 指标的平均值 | 58.06                    | 55.51 | 68.82        |  49.22   |
| high-cpu-all          | 一个指标高于所有主机阈值的所有读数                                                | 122.87                   | 74.76 | 90.04        |     |
| high-cpu-1            | 一个指标高于特定主机阈值的所有读数                                                | 5.11                     | 8.16  | 11.53        |     |
| lastpoint             | 每个主机的最后读数                                                                | 32.34                    | 48.73 | 55.30        |     |
| groupby-orderby-limit | 随机选择的终点之前的最后 5 个汇总读数（跨时间）                                   | 10.63                    | 24.14 | 29.24        |     |


（每 5 分钟一次？ 检查语句似乎是每分钟）


clickhouse 相比 doris 在指标查询上，一般都快一倍，不过似乎在更大数据量的case上，doris 反而变相更良好，例如 high-cpu-all， cpu-max-all-8，double-groupby-all。
过滤效率的差异？ clickhouse 索引空间换来的查询性能？

varint 对于过滤影响不大，主要参与分组聚合、排序字段时，cast函数带来了额外开销，导致查询耗时增加。


VictoriaMetrics 最后4个case不支持，原因参考tsbs的readme。

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


- 各列的存储空间大小，占比
- 不同编码格式
- 高、低基数影响
- 数据类型影响（time, float64）

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

手动再执行 lz4 压缩， 55.69%
159M 88ca94d8-2af6-45ce-a7bb-2bf7680f42b3.tar.lz4

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


调优编码：
- created_date Date DEFAULT today()
- Float64 CODEC(Gorilla)

```
cpu	/var/lib/clickhouse/store/541/541ef9a8-7904-47fe-bfd8-d44c6feacf16/
disk	/var/lib/clickhouse/store/f6c/f6cd9b9c-94a4-40d6-8fcd-cf96d6003155/
diskio	/var/lib/clickhouse/store/c87/c872b906-10c3-4c1e-850e-52158a5de117/
kernel	/var/lib/clickhouse/store/7cc/7cce17a5-2da1-4e00-a5b7-b59c8e237846/
mem	/var/lib/clickhouse/store/fae/fae47377-8207-4697-91b9-998cf7cde1fc/
net	/var/lib/clickhouse/store/e51/e518bbaf-087f-4085-8a73-003782806518/
nginx	/var/lib/clickhouse/store/5d9/5d9c574a-4b82-47c8-bfd0-ee53f65420ab/
postgresl	/var/lib/clickhouse/store/c4d/c4dd4625-22be-496e-ac9d-3a8686dfaf3f/
redis	/var/lib/clickhouse/store/177/17782c60-beaa-4e2a-9cb6-e30da9523dff/
tags	/var/lib/clickhouse/store/216/2165ffd4-716d-41b0-993e-4e219d1eb541/


130M	/var/lib/clickhouse/store/541/541ef9a8-7904-47fe-bfd8-d44c6feacf16/
110M	/var/lib/clickhouse/store/f6c/f6cd9b9c-94a4-40d6-8fcd-cf96d6003155/
220M	/var/lib/clickhouse/store/c87/c872b906-10c3-4c1e-850e-52158a5de117/
158M	/var/lib/clickhouse/store/7cc/7cce17a5-2da1-4e00-a5b7-b59c8e237846/
475M	/var/lib/clickhouse/store/fae/fae47377-8207-4697-91b9-998cf7cde1fc/
236M	/var/lib/clickhouse/store/e51/e518bbaf-087f-4085-8a73-003782806518/
119M	/var/lib/clickhouse/store/5d9/5d9c574a-4b82-47c8-bfd0-ee53f65420ab/
103M	/var/lib/clickhouse/store/c4d/c4dd4625-22be-496e-ac9d-3a8686dfaf3f/
370M	/var/lib/clickhouse/store/177/17782c60-beaa-4e2a-9cb6-e30da9523dff/
84K	/var/lib/clickhouse/store/216/2165ffd4-716d-41b0-993e-4e219d1eb541/

cpu：

total： 133112 K = 130 MB

time 50080 KB = 48.9 MB

50080 .time.bin
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
708 .data.bin
228 .tags_id.bin
120 .created_date.bin
64 .serialization.json
64 .primary.cidx
64 .partition.dat
64 .minmax_created_date.idx
64 .metadata_version.txt
64 .default_compression_codec.txt
64 .count.txt
64 .columns.txt
64 .checksums.txt
56 .usage_user.cmrk2
56 .usage_system.cmrk2
56 .usage_steal.cmrk2
56 .usage_softirq.cmrk2
56 .usage_nice.cmrk2
56 .usage_irq.cmrk2
56 .usage_iowait.cmrk2
56 .usage_idle.cmrk2
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

0.376225 .time.bin
0.0597692 .usage_user.bin
0.0594988 .usage_steal.bin
0.0594387 .usage_irq.bin
0.0594387 .usage_idle.bin
0.0593485 .usage_guest_nice.bin
0.0593185 .usage_nice.bin
0.0592884 .usage_system.bin
0.0592283 .usage_softirq.bin
0.0591983 .usage_guest.bin
0.0591382 .usage_iowait.bin
0.0100667 .created_at.bin
0.00531883 .data.bin
0.00171284 .tags_id.bin
0.000901496 .created_date.bin
0.000480798 .serialization.json
0.000480798 .primary.cidx
0.000480798 .partition.dat
0.000480798 .minmax_created_date.idx
0.000480798 .metadata_version.txt
0.000480798 .default_compression_codec.txt
0.000480798 .count.txt
0.000480798 .columns.txt
0.000480798 .checksums.txt
0.000420698 .usage_user.cmrk2
0.000420698 .usage_system.cmrk2
0.000420698 .usage_steal.cmrk2
0.000420698 .usage_softirq.cmrk2
0.000420698 .usage_nice.cmrk2
0.000420698 .usage_irq.cmrk2
0.000420698 .usage_iowait.cmrk2
0.000420698 .usage_idle.cmrk2
0.000420698 .usage_guest_nice.cmrk2
0.000420698 .usage_guest.cmrk2
0.000420698 .time.cmrk2
0.000420698 .tags_id.cmrk2
0.000420698 .created_date.cmrk2
0.000420698 .created_at.cmrk2
0.000420698 .additional_tags.sparse.idx.cmrk2
0.000420698 .additional_tags.sparse.idx.bin
0.000420698 .additional_tags.cmrk2
6.00998e-05 .data.cmrk3
3.00499e-05 .format_version.txt
0 .additional_tags.bin

find . -type f -exec du -a {} + | awk -F'/' '{print $1 $NF}' | awk '{sum[$2] += $1} END {for (key in sum) print sum[key], key}' | sort -nr  | grep bin$ | awk '{sum +=$1} END {print sum/1024}'

128.473 MB

```

DoubleDelta+LZ4HC(9) 编码 

```
cpu	/var/lib/clickhouse/store/f9e/f9e48964-e5ff-4cac-b45d-479c7f78a752/
disk	/var/lib/clickhouse/store/96e/96e6ba7d-a279-4c00-9573-ca4998ac4d22/
diskio	/var/lib/clickhouse/store/5e2/5e24528f-fe67-4999-adbb-0784bbc7fcbf/
kernel	/var/lib/clickhouse/store/96f/96f3a85a-8322-48c2-a597-d773133d1ce5/
mem	/var/lib/clickhouse/store/ce7/ce73b4bf-59f7-4b6d-8ebe-b9571964a166/
net	/var/lib/clickhouse/store/9a7/9a76e5c1-d19a-4a3b-a71a-e5dbe7357899/
nginx	/var/lib/clickhouse/store/aa5/aa50fc31-249f-4865-b4bf-5d21b602c448/
postgresl	/var/lib/clickhouse/store/a9b/a9bff97d-d81f-40b7-825c-4c49638f5938/
redis	/var/lib/clickhouse/store/812/812e5d86-57d7-4b7d-8135-c4e0b765da97/
tags	/var/lib/clickhouse/store/805/805c8929-204d-4a77-af7e-e76f905b45a4/

153M	/var/lib/clickhouse/store/f9e/f9e48964-e5ff-4cac-b45d-479c7f78a752/
134M	/var/lib/clickhouse/store/96e/96e6ba7d-a279-4c00-9573-ca4998ac4d22/
317M	/var/lib/clickhouse/store/5e2/5e24528f-fe67-4999-adbb-0784bbc7fcbf/
230M	/var/lib/clickhouse/store/96f/96f3a85a-8322-48c2-a597-d773133d1ce5/
537M	/var/lib/clickhouse/store/ce7/ce73b4bf-59f7-4b6d-8ebe-b9571964a166/
344M	/var/lib/clickhouse/store/9a7/9a76e5c1-d19a-4a3b-a71a-e5dbe7357899/
158M	/var/lib/clickhouse/store/aa5/aa50fc31-249f-4865-b4bf-5d21b602c448/
163M	/var/lib/clickhouse/store/a9b/a9bff97d-d81f-40b7-825c-4c49638f5938/
1001M	/var/lib/clickhouse/store/812/812e5d86-57d7-4b7d-8135-c4e0b765da97/
84K	/var/lib/clickhouse/store/805/805c8929-204d-4a77-af7e-e76f905b45a4/


cpu：
total  156508 KB = 152.84 MB

50080 .time.bin
10236 .usage_user.bin
10236 .usage_idle.bin
10236 .usage_guest.bin
10232 .usage_iowait.bin
10232 .usage_guest_nice.bin
10228 .usage_system.bin
10228 .usage_nice.bin
10224 .usage_softirq.bin
10220 .usage_steal.bin
10216 .usage_irq.bin
1340 .created_at.bin
840 .data.bin
228 .tags_id.bin
120 .created_date.bin
64 .serialization.json
64 .primary.cidx
64 .partition.dat
64 .minmax_created_date.idx
64 .metadata_version.txt
64 .default_compression_codec.txt
64 .count.txt
64 .columns.txt
64 .checksums.txt
56 .usage_user.cmrk2
56 .usage_system.cmrk2
56 .usage_steal.cmrk2
56 .usage_softirq.cmrk2
56 .usage_nice.cmrk2
56 .usage_irq.cmrk2
56 .usage_iowait.cmrk2
56 .usage_idle.cmrk2
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


no partition:

cpu	/var/lib/clickhouse/store/687/687bdaaf-3778-46ae-a76c-ca9a0b8bad36/
disk	/var/lib/clickhouse/store/953/953cf72c-4077-455b-b7f5-aa8cc83f94f5/
diskio	/var/lib/clickhouse/store/b5c/b5c20974-fe89-4a20-bfd4-60ffe57bc955/
kernel	/var/lib/clickhouse/store/ed5/ed5f7740-3fb8-457d-8b83-c6d55301df67/
mem	/var/lib/clickhouse/store/5cf/5cffdba1-4c2c-454d-a8f0-8b09fd0e52b4/
net	/var/lib/clickhouse/store/eb6/eb6cf846-1279-417f-8756-f1941cb5bcfa/
nginx	/var/lib/clickhouse/store/be9/be91f72d-bc0d-4bed-a2ac-70bdf668cd91/
postgresl	/var/lib/clickhouse/store/2bd/2bd7ee58-1c84-4f5b-a8aa-f06cc0928c1d/
redis	/var/lib/clickhouse/store/25f/25fac2b9-cc59-4a68-b61b-1b37032a9197/
tags	/var/lib/clickhouse/store/0e8/0e89e67a-ba09-4abb-addb-4b5ad87da8bf/

273M	/var/lib/clickhouse/store/687/687bdaaf-3778-46ae-a76c-ca9a0b8bad36/
156M	/var/lib/clickhouse/store/953/953cf72c-4077-455b-b7f5-aa8cc83f94f5/
364M	/var/lib/clickhouse/store/b5c/b5c20974-fe89-4a20-bfd4-60ffe57bc955/
269M	/var/lib/clickhouse/store/ed5/ed5f7740-3fb8-457d-8b83-c6d55301df67/
585M	/var/lib/clickhouse/store/5cf/5cffdba1-4c2c-454d-a8f0-8b09fd0e52b4/
403M	/var/lib/clickhouse/store/eb6/eb6cf846-1279-417f-8756-f1941cb5bcfa/
185M	/var/lib/clickhouse/store/be9/be91f72d-bc0d-4bed-a2ac-70bdf668cd91/
113M	/var/lib/clickhouse/store/2bd/2bd7ee58-1c84-4f5b-a8aa-f06cc0928c1d/
629M	/var/lib/clickhouse/store/25f/25fac2b9-cc59-4a68-b61b-1b37032a9197/
76K	/var/lib/clickhouse/store/0e8/0e89e67a-ba09-4abb-addb-4b5ad87da8bf/


cpu:

usage_* 219.445 MB

51252 .time.bin
22484 .usage_idle.bin
22484 .usage_guest_nice.bin
22476 .usage_steal.bin
22476 .usage_iowait.bin
22472 .usage_user.bin
22472 .usage_guest.bin
22468 .usage_nice.bin
22468 .usage_irq.bin
22464 .usage_system.bin
22448 .usage_softirq.bin
1492 .data.bin
1312 .created_at.bin
196 .tags_id.bin
104 .created_date.bin
20 .serialization.json
20 .primary.cidx
20 .metadata_version.txt
20 .default_compression_codec.txt
20 .count.txt
20 .columns.txt
20 .checksums.txt
20 .additional_tags.sparse.idx.bin
16 .usage_user.cmrk2
16 .usage_system.cmrk2
16 .usage_steal.cmrk2
16 .usage_softirq.cmrk2
16 .usage_nice.cmrk2
16 .usage_irq.cmrk2
16 .usage_iowait.cmrk2
16 .usage_idle.cmrk2
16 .usage_guest_nice.cmrk2
16 .usage_guest.cmrk2
16 .time.cmrk2
16 .tags_id.cmrk2
16 .created_date.cmrk2
16 .created_at.cmrk2
16 .additional_tags.sparse.idx.cmrk2
16 .additional_tags.cmrk2
4 .format_version.txt
4 .data.cmrk3
0 .additional_tags.bin

gorilla + lz4:

cpu	/var/lib/clickhouse/store/e19/e190f911-571a-44db-8e07-e5c27743e2ab/
disk	/var/lib/clickhouse/store/dc6/dc6c0fff-d76b-4ddb-9266-7b8b75148dab/
diskio	/var/lib/clickhouse/store/fad/fad49454-f8e8-4cb0-9c5a-2daf5c5bb5d0/
kernel	/var/lib/clickhouse/store/274/274ddd4d-a94f-4d56-98eb-72d239d94e25/
mem	/var/lib/clickhouse/store/1ff/1ff64252-1d26-4a33-8f84-a756de6cda14/
net	/var/lib/clickhouse/store/4d4/4d40377e-3e92-40ce-bfaf-ad49edac3abd/
nginx	/var/lib/clickhouse/store/00d/00db979e-17fe-419e-b9e2-e7f4b71c4a4e/
postgresl	/var/lib/clickhouse/store/188/1882842d-a884-4d1a-9556-651306571fb6/
redis	/var/lib/clickhouse/store/f1e/f1efd317-4996-4d09-9190-19fed51cc290/
tags	/var/lib/clickhouse/store/1b1/1b148f01-8e1d-4298-9b42-4581dea6a0f9/


129M	/var/lib/clickhouse/store/e19/e190f911-571a-44db-8e07-e5c27743e2ab/
98M	/var/lib/clickhouse/store/dc6/dc6c0fff-d76b-4ddb-9266-7b8b75148dab/
192M	/var/lib/clickhouse/store/fad/fad49454-f8e8-4cb0-9c5a-2daf5c5bb5d0/
136M	/var/lib/clickhouse/store/274/274ddd4d-a94f-4d56-98eb-72d239d94e25/
467M	/var/lib/clickhouse/store/1ff/1ff64252-1d26-4a33-8f84-a756de6cda14/
207M	/var/lib/clickhouse/store/4d4/4d40377e-3e92-40ce-bfaf-ad49edac3abd/
105M	/var/lib/clickhouse/store/00d/00db979e-17fe-419e-b9e2-e7f4b71c4a4e/
75M	/var/lib/clickhouse/store/188/1882842d-a884-4d1a-9556-651306571fb6/
282M	/var/lib/clickhouse/store/f1e/f1efd317-4996-4d09-9190-19fed51cc290/
76K	/var/lib/clickhouse/store/1b1/1b148f01-8e1d-4298-9b42-4581dea6a0f9/


cpu:

51252 .time.bin
7732 .usage_steal.bin
7720 .usage_nice.bin
7720 .usage_irq.bin
7716 .usage_system.bin
7712 .usage_user.bin
7712 .usage_softirq.bin
7704 .usage_guest.bin
7696 .usage_idle.bin
7696 .usage_guest_nice.bin
7692 .usage_iowait.bin
1312 .created_at.bin
700 .data.bin
196 .tags_id.bin
104 .created_date.bin
20 .serialization.json
20 .primary.cidx
20 .metadata_version.txt
20 .default_compression_codec.txt
20 .count.txt
20 .columns.txt
20 .checksums.txt
20 .additional_tags.sparse.idx.bin
16 .usage_user.cmrk2
16 .usage_system.cmrk2
16 .usage_steal.cmrk2
16 .usage_softirq.cmrk2
16 .usage_nice.cmrk2
16 .usage_irq.cmrk2
16 .usage_iowait.cmrk2
16 .usage_idle.cmrk2
16 .usage_guest_nice.cmrk2
16 .usage_guest.cmrk2
16 .time.cmrk2
16 .tags_id.cmrk2
16 .created_date.cmrk2
16 .created_at.cmrk2
16 .additional_tags.sparse.idx.cmrk2
16 .additional_tags.cmrk2
4 .format_version.txt
4 .data.cmrk3
0 .additional_tags.bin


float32 + gorilla + lz4

cpu	/var/lib/clickhouse/store/5e7/5e77c159-591c-4382-8441-7d554d2d7cf0/
disk	/var/lib/clickhouse/store/a41/a4162208-0497-48e0-8e83-43f82865e722/
diskio	/var/lib/clickhouse/store/c0a/c0ae228b-d2cb-4912-a4f3-8767f77b0a99/
kernel	/var/lib/clickhouse/store/3ea/3ea514c9-4f5e-4e49-b8d6-90e6f5395264/
mem	/var/lib/clickhouse/store/0da/0da3903a-46e9-4bb5-8a10-c4a844ed970e/
net	/var/lib/clickhouse/store/5ce/5ce54c75-9e53-42e3-9831-b806f7f3da8c/
nginx	/var/lib/clickhouse/store/562/5626ad77-e274-4367-bad9-26879c09a71d/
postgresl	/var/lib/clickhouse/store/3c2/3c2ede75-322d-44f7-b8df-a284e4671694/
redis	/var/lib/clickhouse/store/e64/e6400e69-f415-4b2e-a85c-b1f393d25818/
tags	/var/lib/clickhouse/store/6b4/6b4c3134-e5d7-49b1-8a71-805e01056dc5/


127M	/var/lib/clickhouse/store/5e7/5e77c159-591c-4382-8441-7d554d2d7cf0/
55M	/var/lib/clickhouse/store/a41/a4162208-0497-48e0-8e83-43f82865e722/
190M	/var/lib/clickhouse/store/c0a/c0ae228b-d2cb-4912-a4f3-8767f77b0a99/
135M	/var/lib/clickhouse/store/3ea/3ea514c9-4f5e-4e49-b8d6-90e6f5395264/
371M	/var/lib/clickhouse/store/0da/0da3903a-46e9-4bb5-8a10-c4a844ed970e/
203M	/var/lib/clickhouse/store/5ce/5ce54c75-9e53-42e3-9831-b806f7f3da8c/
103M	/var/lib/clickhouse/store/562/5626ad77-e274-4367-bad9-26879c09a71d/
73M	/var/lib/clickhouse/store/3c2/3c2ede75-322d-44f7-b8df-a284e4671694/
199M	/var/lib/clickhouse/store/e64/e6400e69-f415-4b2e-a85c-b1f393d25818/
76K	/var/lib/clickhouse/store/6b4/6b4c3134-e5d7-49b1-8a71-805e01056dc5/


cpu：


51252 .time.bin
7564 .usage_steal.bin
7548 .usage_nice.bin
7544 .usage_irq.bin
7544 .usage_guest_nice.bin
7540 .usage_user.bin
7536 .usage_guest.bin
7532 .usage_system.bin
7532 .usage_softirq.bin
7532 .usage_iowait.bin
7532 .usage_idle.bin
1312 .created_at.bin
696 .data.bin
196 .tags_id.bin
104 .created_date.bin
20 .serialization.json
20 .primary.cidx
20 .metadata_version.txt
20 .default_compression_codec.txt
20 .count.txt
20 .columns.txt
20 .checksums.txt
20 .additional_tags.sparse.idx.bin
16 .usage_user.cmrk2
16 .usage_system.cmrk2
16 .usage_steal.cmrk2
16 .usage_softirq.cmrk2
16 .usage_nice.cmrk2
16 .usage_irq.cmrk2
16 .usage_iowait.cmrk2
16 .usage_idle.cmrk2
16 .usage_guest_nice.cmrk2
16 .usage_guest.cmrk2
16 .time.cmrk2
16 .tags_id.cmrk2
16 .created_date.cmrk2
16 .created_at.cmrk2
16 .additional_tags.sparse.idx.cmrk2
16 .additional_tags.cmrk2
4 .format_version.txt
4 .data.cmrk3
0 .additional_tags.bin


usage* 75404 KB = 73.63 MB 
与 oris (66.115MB) 相差不大了


float32 + lz4

cpu	/var/lib/clickhouse/store/875/8750a536-006f-4155-bc5b-be6219ee2a1f/
disk	/var/lib/clickhouse/store/94e/94e3efa9-bafe-4d61-91f1-9f4f40d65df7/
diskio	/var/lib/clickhouse/store/52a/52a902a1-4100-4c15-8a8f-b1016251f30d/
kernel	/var/lib/clickhouse/store/c76/c76450f3-9f60-4883-bdb2-b7bd58ee7854/
mem	/var/lib/clickhouse/store/1ec/1ecf7109-5f56-4af5-bc0c-c99228cafbcb/
net	/var/lib/clickhouse/store/ad3/ad32f555-dcc1-4d59-b193-854cddacfe65/
nginx	/var/lib/clickhouse/store/005/0059d131-6eda-4a7d-812a-45f0e8e7dbf8/
postgresl	/var/lib/clickhouse/store/aab/aab9845b-9965-4a0a-b590-ef6cd3aa9685/
redis	/var/lib/clickhouse/store/4f1/4f1e5ace-6970-41d1-b43e-062ae7728a15/
tags	/var/lib/clickhouse/store/738/7382cf32-bfd4-4fe8-be01-0db6af291a90/

264M	/var/lib/clickhouse/store/875/8750a536-006f-4155-bc5b-be6219ee2a1f/
56M	/var/lib/clickhouse/store/94e/94e3efa9-bafe-4d61-91f1-9f4f40d65df7/
328M	/var/lib/clickhouse/store/52a/52a902a1-4100-4c15-8a8f-b1016251f30d/
247M	/var/lib/clickhouse/store/c76/c76450f3-9f60-4883-bdb2-b7bd58ee7854/
367M	/var/lib/clickhouse/store/1ec/1ecf7109-5f56-4af5-bc0c-c99228cafbcb/
366M	/var/lib/clickhouse/store/ad3/ad32f555-dcc1-4d59-b193-854cddacfe65/
172M	/var/lib/clickhouse/store/005/0059d131-6eda-4a7d-812a-45f0e8e7dbf8/
100M	/var/lib/clickhouse/store/aab/aab9845b-9965-4a0a-b590-ef6cd3aa9685/
598M	/var/lib/clickhouse/store/4f1/4f1e5ace-6970-41d1-b43e-062ae7728a15/
76K	/var/lib/clickhouse/store/738/7382cf32-bfd4-4fe8-be01-0db6af291a90/


51248 .time.bin
21516 .usage_guest_nice.bin
21512 .usage_iowait.bin
21508 .usage_idle.bin
21504 .usage_steal.bin
21496 .usage_user.bin
21496 .usage_system.bin
21496 .usage_guest.bin
21492 .usage_nice.bin
21492 .usage_irq.bin
21472 .usage_softirq.bin
1444 .data.bin
1312 .created_at.bin
196 .tags_id.bin
104 .created_date.bin
20 .serialization.json
20 .primary.cidx
20 .metadata_version.txt
20 .default_compression_codec.txt
20 .count.txt
20 .columns.txt
20 .checksums.txt
20 .additional_tags.sparse.idx.bin
16 .usage_user.cmrk2
16 .usage_system.cmrk2
16 .usage_steal.cmrk2
16 .usage_softirq.cmrk2
16 .usage_nice.cmrk2
16 .usage_irq.cmrk2
16 .usage_iowait.cmrk2
16 .usage_idle.cmrk2
16 .usage_guest_nice.cmrk2
16 .usage_guest.cmrk2
16 .time.cmrk2
16 .tags_id.cmrk2
16 .created_date.cmrk2
16 .created_at.cmrk2
16 .additional_tags.sparse.idx.cmrk2
16 .additional_tags.cmrk2
4 .format_version.txt
4 .data.cmrk3
0 .additional_tags.bin


usage*  214984 KB = 209.9MB

```



clickhouse time 字段（2016-01-01 08:00:00 +0800）空间开销过高


###### 时间类型对比：

DoubleDelta vs lz4:

使用 cpu 表分析

对于时间戳类型 DoubleDelta 更有优势 (9.35X) ，created_date 日期类型 lz4 压缩更好  


| 编码格式        | created_at(KB) | created_date(KB) | sum       | 比例     |
|-----------------|----------------|------------------|-----------|----------|
| DoubleDelta<br> | 1340<br>       | 1300<br>         | 2640<br>  | 1.81<br> |
| lz4<br>         | 12528<br>      | 100<br>          | 12628<br> | 8.65<br> |
| 混合优化<br>    | 1340<br>       | 120<br>          | 1460<br>  | 1.0<br>  |




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


估计 10 字段 大约 

lz4 空间消耗是 Gorilla 1.25X, Gorilla null文件为什么开销大？

理论数据计算fiels空间大小：

cpu 单表 10368000 行，Float64 8B， 10 fields

10368000 * 8B * 10 = 791 MB

实际：

lz4 约等于 220 MB

Gorilla + null 约等于 176 MB

Gorilla 约等于 77.7 MB


字段对比

| 编码格式         | usage_user(KB) | null(KB) | sum (KB) | 压缩比 |
|------------------|----------------|----------|----------|--------|
| Gorilla+nullable | 7956           | 10104    | 18060    | 2.27   |
| lz4              | 22520          | 56       | 22576    | 2.84   |
| Gorilla          | 7956           | 0        | 7956     | 1.0    |
| LZ4HC            | 10236          | 0        | 10236    | 1.29   |


导入性能：测试导入时使用 Gorilla编码时，cpu负载不高，也许由于依赖顺序编码未能充分利用多线程工作（并发导入可能写入性能会提高）



ck的其他支持编码优化：

- LowCardinality(String) 低基数，将使用基于字典的编码
- COLUMN `time` CODEC(Delta, ZSTD)

| 表        | doris     | gorilla | gorilla+lz4 | gorilla+lz4+float32 | 压缩比(gorilla/doris) | 压缩比(float32/doris) |
|-----------|-----------|---------|---------------|-------------------------|-----------------------|-----------------------|
| cpu       | 70.401    | 130     | 129           | 127                     | 1.85                  | 1.80                  |
| disk      | 8.727     | 110     | 98            | 56                      | 12.60                 | 6.42                  |
| diskio    | 93.106    | 220     | 192           | 190                     | 2.36                  | 2.04                  |
| kernel    | 61.714    | 158     | 136           | 135                     | 2.56                  | 2.19                  |
| mem       | 242.317   | 475     | 467           | 371                     | 1.96                  | 1.53                  |
| net       | 103.649   | 236     | 207           | 203                     | 2.28                  | 1.96                  |
| nginx     | 40.802    | 119     | 105           | 103                     | 2.92                  | 2.52                  |
| postgresl | 17.584    | 103     | 75            | 73                      | 5.86                  | 4.15                  |
| redis     | 112.202   | 370     | 282           | 199                     | 3.30                  | 1.77                  |
| tags      | 11.152 KB | 84K     | 76K           | 76K                     | 7.53                  | 6.81                  |





gorilla+lz4+float32编码设置下：

ck time 字段 占据 50MB，
cpu,disk,kernel，nginx， postgresl，redis 表 接近

diskio reads、writes 字段 变动较大 gorilla 效果不够好，reads 字段 ndv 数量为 1,294,179

mem 表 used_percent（827 6228），available（872 6303） 重复度不高。doris和ck压缩效率都降低。
（doris bitshuffle + lz4）


```
50888 .time.bin
40992 .free.bin
40992 .available.bin
40960 .cached.bin
40924 .buffered.bin
40916 .used.bin
40572 .available_percent.bin
40432 .used_percent.bin
40424 .buffered_percent.bin
1336 .created_at.bin
204 .tags_id.bin
108 .created_date.bin
60 .total.bin
24 .additional_tags.sparse.idx.bin
0 .additional_tags.bin


free，40992 字段等 空间开销高
total 字段 3 个 ndv 值
```


#### doris 存储分析



```
mysql> SELECT table_name, data_length/1024/1024 AS total_size,TABLE_ROWS FROM information_schema.tables WHERE table_schema = 'benchmark' order by total_size;
+-------------+----------------------+------------+
| table_name  | total_size           | TABLE_ROWS |
+-------------+----------------------+------------+
| tags        | 0.010890960693359375 |       1200 |
| devops_disk |    8.727141380310059 |   10368000 |
| postgresl   |   17.584471702575684 |   10368000 |
| nginx       |    40.80240345001221 |   10368000 |
| kernel      |    61.71394729614258 |   10368000 |
| cpu         |     70.4008436203003 |   10368000 |
| diskio      |    93.10633373260498 |   10368000 |
| net         |   103.64865684509277 |   10368000 |
| redis       |   112.20183277130127 |   10368000 |
| mem         |   242.31737899780273 |   10368000 |
+-------------+----------------------+------------+


由于非单列存储，无法获取各列的空间大小

SHOW TABLETS FROM benchmark.cpu\G;
               TabletId: 27195
              ReplicaId: 27196
              BackendId: 12172
             SchemaHash: 415384547
                Version: 2
      LstSuccessVersion: 2
       LstFailedVersion: -1
          LstFailedTime: NULL
          LocalDataSize: 73820635
         RemoteDataSize: 0
               RowCount: 10368000
                  State: NORMAL
LstConsistencyCheckTime: NULL
           CheckVersion: -1
           VersionCount: 2
              QueryHits: 0
               PathHash: 2715812420580570149
                   Path: /home/tianjiqx/tmp/apache-doris-2.1.3-bin-x64/be/storage
                MetaUrl: http://192.168.111.154:8040/api/meta/header/27195
       CompactionStatus: http://192.168.111.154:8040/api/compaction/show?tablet_id=27195
      CooldownReplicaId: -1
         CooldownMetaId: 


MetaUrl 可观察到 使用默认压缩类型 "compression_type": "LZ4F", "num_rows_per_row_block": 1024,


```

ck和doris 表空间大小对比
​
| 表        | doris(MB) | ck调优(MB) | 压缩比 |
|-----------|-----------|------------|--------|
| cpu       | 70.401    | 130        | 1.85   |
| disk      | 8.727     | 110        | 12.60  |
| diskio    | 93.106    | 220        | 2.36   |
| kernel    | 61.714    | 158        | 2.56   |
| mem       | 242.317   | 475        | 1.96   |
| net       | 103.649   | 236        | 2.28   |
| nginx     | 40.802    | 119        | 2.92   |
| postgresl | 17.584    | 103        | 5.86   |
| redis     | 112.202   | 370        | 3.30   |
| tags      | 11.152 KB | 84K        | 7.53   |


cpu表：

doris移除掉 float 的fields 字段后， 空间大小为 4.286 MB， 推算可得， doris 在其他字段usage上消耗空间为 66.115。

cpu 表 单列 usage_user 减去base 计算得 6.576 MB，比下面 lz4 直接压缩更低。

ck Gorilla 对应的​ usage字段，消耗空间为 77.1719，在 float 类型字段空间消耗差异不大。（ck分区而doris未分区影响？测试无分区的lz4 219.445，影响不大）
ck lz4 编码 对应的​ usage字段，消耗空间为 220.445。



手动测试：

usage_user 单列，29M， 10列usage字段，287M。逐一按照列存追加成单文本文件（非float字节数组），手动使用 lz4 压缩

|            | 原始size（MB） | lz4 size（MB） | 压缩 |
|------------|--------------|--------------|--------|
| usage_user（4MB） | 29           | 13           | 42.79%/2.23 |
| usage_*  （4MB）   | 287          | 123          | 42.79%/2.23 |
| usage_*  （64KB）   | 287          | 133          | 46.20%/2.16 |


使用如下sql导出的 usage_user 列大小为 14M， 与 文本lz4压缩大小一致。 
```
SELECT usage_user FROM benchmark2.cpu INTO OUTFILE 'usage_user.native.lz4.bin' COMPRESSION 'lz4'  FORMAT Native
SELECT usage_user FROM benchmark2.cpu INTO OUTFILE 'usage_user.RowBinary.lz4.bin' COMPRESSION 'lz4'  FORMAT RowBinary
```

ck 默认压缩块大小是 64K， doris 默认也是 64K.


对比，实际 ck 压缩大小（220.445MB），未达到 lz4 的理想（133MB）效果。并且，doris (66.115MB) 实际还要比 lz4 理想压缩空间更小一半左右。
根据手动lz4 对ck 数据 目录执行 打包并lz4 压缩，可以再压缩一半空间。

**问题：**
- ck 的 lz4 压缩不够理想的原因？（版本实现？）
- doris 压缩率更高原因？（在lz4 压缩前，是否还执行过其他编码， DecomposedFloat？）

!!! 
doris 建表语句使用了 FLOAT 默认，是 4 字节， ck float64 类型是 8 字节


// 使用float32二进制存储usage_user字段，空间 10368000*4/1024/1024 = 39.5MB

usage_user 列：

|                 | 压缩结果 | 压缩比 |
|-----------------|-----------------|--------|
| lz4 size（1MB块） | 23M             | 1.7    |
| bigshuffle+lz4 size（1MB块） | 6.3M   | 6.3    |

bigshuffle+lz4 测试 6.3M 与 doris 的大小 6.576 MB 基本一致，每个 float 数据占据6.3MB / 10368000 = 0.637 B
（注意，实际usage_user字段，是int类型）

VictoriaMetrics的改进Gorilla声称将典型的node_exporter时间序列数据压缩到每个数据点0.4字节。


用随机数生成(最坏情况，高熵数据（即具有大量小数位的随机数），真实情况两个值会接近)，100个不同的1M flaot 值：
```java
private static float[] generateFloatData(int size) {
    Random random = new Random();
    float[] data = new float[size];
    for (int i = 0; i < size; i++) {
        data[i] = random.nextLong() % 100 / 10.0f;
    }
    return data;
}

/*
Original size: 4000000 bytes
LZ4 size: 2337920 bytes
BitShuffle + LZ4 size: 1955675 bytes
LZ4 compression ratio: 1.71
BitShuffle + LZ4 compression ratio: 2.05
LZ4 compression time: 31.51 ms
BitShuffle + LZ4 compression time: 19.70 ms
LZ4 compression speed: 121.06 MB/s
BitShuffle + LZ4 compression speed: 193.60 MB/s

// 去除 / 10.0f 后
Original size: 4000000 bytes
LZ4 size: 2070649 bytes
BitShuffle + LZ4 size: 1363041 bytes
LZ4 compression ratio: 1.93
BitShuffle + LZ4 compression ratio: 2.93
LZ4 compression time: 30.32 ms
BitShuffle + LZ4 compression time: 19.70 ms
LZ4 compression speed: 125.82 MB/s
BitShuffle + LZ4 compression speed: 193.69 MB/s

*/
```
BitShuffle 额外增加的bit转换，甚至可以提升lz4执行效率！

disk表：

基本是低基数字段， 字典编码压缩效率可以很高
```
select count(distinct(used)),count(distinct(free)),count(distinct(free)) from disk;
+----------------------+----------------------+----------------------+
| count(DISTINCT used) | count(DISTINCT free) | count(DISTINCT free) |
+----------------------+----------------------+----------------------+
|                   41 |                   21 |                   21 |
```

ck Gorilla 编码 disk 各个列文件大小
```
47324 .time.bin
27484 .used.bin
24784 .free.bin
1728 .additional_tags.bin
1516 .inodes_used.bin
1472 .inodes_free.bin
1344 .used_percent.bin
1344 .total.bin
1344 .inodes_total.bin
1336 .created_at.bin
352 .data.bin
220 .tags_id.bin
124 .created_date.bin

```

ck lz4 

```
49056 .free.bin
48740 .used.bin
41680 .time.bin
12768 .created_at.bin
1704 .additional_tags.bin
1164 .inodes_used.bin
1164 .inodes_free.bin
852 .data.bin
388 .used_percent.bin
384 .total.bin
384 .inodes_total.bin
208 .tags_id.bin
104 .created_date.bin
56 .used_percent.null.bin
56 .used.null.bin
56 .total.null.bin
56 .inodes_used.null.bin
56 .inodes_total.null.bin
56 .inodes_free.null.bin
56 .free.null.bin

```

ck 默认lz4  是无字典参数？ LZ4HC(level:1-12)

ck 按照日期拆分出多个目录，是否也导致压缩效率不高？

cpu表，字段值实际是int值，并且范围很低（0-100），是否也导致实际可以利用字典，提高压缩率



LowCardinality(Float64) 未起作用？

| 表        | doris(MB) | ck(LowCardinality) | 压缩比 |
|-----------|-----------|--------------------|--------|
| cpu       | 70.401    | 128.41             | 1.82   |
| disk      | 8.727     | 174.97             | 20.05  |
| diskio    | 93.106    | 433.13             | 4.65   |
| kernel    | 61.714    | 297.68             | 4.82   |
| mem       | 242.317   | 694.48             | 2.87   |
| net       | 103.649   | 448.86             | 4.33   |
| nginx     | 40.802    | 191.58             | 4.70   |
| postgresl | 17.584    | 110.12             | 6.26   |
| redis     | 112.202   | 646.64             | 5.76   |
| tags      | 11.152 KB | 25.6               | 2.30   |
​


FCBench: Cross-Domain Benchmarking of Lossless Compression for Floating-Point Data [Experiment, Analysis & Benchmark]

- 压缩效果
HPC数据使用fpzip
时间序列数据使用nvCOMP:LZ4
观察数据使用bitshuffle:zstd
tpc-x数据库数据使用Chimp

- 压缩、解压速度
bitshuffle:LZ4、bitshuffle:zstd、MPC和ndzip-CPU/GPU

总体而言，bitshuffle方法由于其更好的鲁棒性和更低的CPU硬件成本而成为首选

doris,kudu 选对了 bitshuffle + lz4 就是好。用tsbs测试 也确实比ck好。



doris datetime 默认也使用 BIT_SHUFFLE + lz4 编码压缩 


### ES 存储分析

基于 ES 6.8 的指标存储实现

total 10.8 GB

| field                             | type          | total    | total_pct | inverted_index | stored_field | doc_values | points  | term_vectors | norms |
| --------------------------------- | ------------- | -------- | --------- | -------------- | ------------ | ---------- | ------- | ------------ | ----- |
| _id                               | unknown       | 1.3gb    | 12.30%    | 899.6mb        | 469.1mb      | 0b         | 0b      | 0b           | 0b    |
| _tag_names                        | array\<string> | 1.2gb    | 11.19%    | 0b             | 0b           | 1.2gb      | 0b      | 0b           | 0b    |
| _metric_names                     | array\<string> | 1012.2mb | 9.10%     | 0b             | 0b           | 1012.2mb   | 0b      | 0b           | 0b    |
| _seq_no                           | unknown       | 698.5mb  | 6.28%     | 0b             | 0b           | 296.1mb    | 402.4mb | 0b           | 0b    |
| _time                             | long          | 418.2mb  | 3.76%     | 0b             | 0b           | 167.7mb    | 250.5mb | 0b           | 0b    |
| host                              | string        | 150.6mb  | 1.35%     | 17.1mb         | 0b           | 133.5mb    | 0b      | 0b           | 0b    |
| _series                           | string        | 134.6mb  | 1.21%     | 0b             | 0b           | 134.6mb    | 0b      | 0b           | 0b    |
| rack                              | array\<string> | 104.3mb  | 0.94%     | 15.3mb         | 0b           | 89.0mb     | 0b      | 0b           | 0b    |
| datacenter                        | array\<string> | 102.5mb  | 0.92%     | 13.5mb         | 0b           | 89.0mb     | 0b      | 0b           | 0b    |
| service                           | array\<string> | 102.2mb  | 0.92%     | 13.2mb         | 0b           | 89.0mb     | 0b      | 0b           | 0b    |
| mem_buffered                      | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| mem_cached                        | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| mem_used                          | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| mem_buffered_percent              | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| mem_free                          | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| mem_used_percent                  | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| mem_available_percent             | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| mem_available                     | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_system                  | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_irq                     | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_user                    | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_idle                    | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_guest_nice              | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_iowait                  | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_softirq                 | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_steal                   | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_guest                   | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| cpu_usage_nice                    | double        | 79.4mb   | 0.71%     | 0b             | 0b           | 79.4mb     | 0b      | 0b           | 0b    |
| redis_instantaneous_output_kbps   | double        | 74.2mb   | 0.67%     | 0b             | 0b           | 74.2mb     | 0b      | 0b           | 0b    |
| redis_instantaneous_input_kbps    | double        | 74.2mb   | 0.67%     | 0b             | 0b           | 74.2mb     | 0b      | 0b           | 0b    |
| redis_instantaneous_ops_per_sec   | double        | 74.2mb   | 0.67%     | 0b             | 0b           | 74.2mb     | 0b      | 0b           | 0b    |
| postgresl_temp_bytes              | double        | 74.1mb   | 0.67%     | 0b             | 0b           | 74.1mb     | 0b      | 0b           | 0b    |
| kernel_processes_forked           | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| kernel_interrupts                 | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| kernel_disk_pages_out             | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| kernel_context_switches           | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| kernel_disk_pages_in              | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| redis_keyspace_hits               | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| redis_expired_keys                | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| redis_evicted_keys                | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| redis_keyspace_misses             | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| redis_total_connections_received  | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| diskio_io_time                    | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| diskio_writes                     | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| diskio_read_bytes                 | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| diskio_reads                      | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| diskio_read_time                  | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| diskio_write_time                 | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| diskio_write_bytes                | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| net_err_in                        | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| net_bytes_sent                    | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| net_packets_recv                  | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| net_err_out                       | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| net_packets_sent                  | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| net_drop_in                       | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| net_bytes_recv                    | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| net_drop_out                      | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| nginx_handled                     | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| nginx_accepts                     | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| nginx_requests                    | double        | 74.0mb   | 0.67%     | 0b             | 0b           | 74.0mb     | 0b      | 0b           | 0b    |
| redis_uptime_in_seconds           | double        | 73.3mb   | 0.66%     | 0b             | 0b           | 73.3mb     | 0b      | 0b           | 0b    |
| region                            | array\<string> | 56.3mb   | 0.51%     | 11.8mb         | 0b           | 44.5mb     | 0b      | 0b           | 0b    |
| redis_used_memory_rss             | double        | 49.6mb   | 0.45%     | 0b             | 0b           | 49.6mb     | 0b      | 0b           | 0b    |
| redis_used_memory_peak            | double        | 49.6mb   | 0.45%     | 0b             | 0b           | 49.6mb     | 0b      | 0b           | 0b    |
| redis_used_memory                 | double        | 49.6mb   | 0.45%     | 0b             | 0b           | 49.6mb     | 0b      | 0b           | 0b    |
| redis_used_memory_lua             | double        | 49.6mb   | 0.45%     | 0b             | 0b           | 49.6mb     | 0b      | 0b           | 0b    |
| origin                            | string        | 48.4mb   | 0.43%     | 3.9mb          | 0b           | 44.5mb     | 0b      | 0b           | 0b    |
| disk_used                         | double        | 46.2mb   | 0.42%     | 0b             | 0b           | 46.2mb     | 0b      | 0b           | 0b    |
| disk_free                         | double        | 44.4mb   | 0.40%     | 0b             | 0b           | 44.4mb     | 0b      | 0b           | 0b    |
| postgresl_numbackends             | double        | 38.7mb   | 0.35%     | 0b             | 0b           | 38.7mb     | 0b      | 0b           | 0b    |
| redis_connected_slaves            | double        | 38.6mb   | 0.35%     | 0b             | 0b           | 38.6mb     | 0b      | 0b           | 0b    |
| postgresl_tup_deleted             | double        | 38.5mb   | 0.35%     | 0b             | 0b           | 38.5mb     | 0b      | 0b           | 0b    |
| redis_sync_partial_err            | double        | 38.5mb   | 0.35%     | 0b             | 0b           | 38.5mb     | 0b      | 0b           | 0b    |
| redis_used_cpu_user               | double        | 38.5mb   | 0.35%     | 0b             | 0b           | 38.5mb     | 0b      | 0b           | 0b    |
| redis_used_cpu_sys_children       | double        | 38.5mb   | 0.35%     | 0b             | 0b           | 38.5mb     | 0b      | 0b           | 0b    |
| postgresl_blks_read               | double        | 38.5mb   | 0.35%     | 0b             | 0b           | 38.5mb     | 0b      | 0b           | 0b    |
| postgresl_tup_fetched             | double        | 38.5mb   | 0.35%     | 0b             | 0b           | 38.5mb     | 0b      | 0b           | 0b    |
| postgresl_blk_write_time          | double        | 38.5mb   | 0.35%     | 0b             | 0b           | 38.5mb     | 0b      | 0b           | 0b    |
| postgresl_temp_files              | double        | 38.4mb   | 0.35%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| redis_latest_fork_usec            | double        | 38.4mb   | 0.35%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| redis_repl_backlog_histlen        | double        | 38.4mb   | 0.35%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| redis_repl_backlog_active         | double        | 38.4mb   | 0.35%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| redis_pubsub_patterns             | double        | 38.4mb   | 0.35%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| redis_master_repl_offset          | double        | 38.4mb   | 0.35%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| postgresl_deadlocks               | double        | 38.4mb   | 0.34%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| postgresl_tup_returned            | double        | 38.4mb   | 0.34%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| postgresl_xact_commit             | double        | 38.4mb   | 0.34%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| postgresl_conflicts               | double        | 38.4mb   | 0.34%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| postgresl_blks_hit                | double        | 38.4mb   | 0.34%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| postgresl_blk_read_time           | double        | 38.4mb   | 0.34%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| redis_used_cpu_user_children      | double        | 38.4mb   | 0.34%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| redis_used_cpu_sys                | double        | 38.4mb   | 0.34%     | 0b             | 0b           | 38.4mb     | 0b      | 0b           | 0b    |
| postgresl_tup_inserted            | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| postgresl_tup_updated             | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| postgresl_xact_rollback           | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| redis_sync_partial_ok             | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| redis_connected_clients           | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| redis_repl_backlog_size           | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| redis_sync_full                   | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| redis_rdb_changes_since_last_save | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| redis_pubsub_channels             | double        | 38.3mb   | 0.34%     | 0b             | 0b           | 38.3mb     | 0b      | 0b           | 0b    |
| server                            | array\<string> | 34.6mb   | 0.31%     | 4.4mb          | 0b           | 30.2mb     | 0b      | 0b           | 0b    |
| port                              | array\<string> | 34.6mb   | 0.31%     | 4.4mb          | 0b           | 30.2mb     | 0b      | 0b           | 0b    |
| team                              | array\<string> | 31.8mb   | 0.29%     | 9.6mb          | 0b           | 22.2mb     | 0b      | 0b           | 0b    |
| os                                | array\<string> | 30.6mb   | 0.27%     | 8.3mb          | 0b           | 22.2mb     | 0b      | 0b           | 0b    |
| service_environment               | array\<string> | 30.4mb   | 0.27%     | 8.2mb          | 0b           | 22.2mb     | 0b      | 0b           | 0b    |
| serial                            | array\<string> | 17.5mb   | 0.16%     | 2.3mb          | 0b           | 15.2mb     | 0b      | 0b           | 0b    |
| arch                              | array\<string> | 17.4mb   | 0.16%     | 6.2mb          | 0b           | 11.1mb     | 0b      | 0b           | 0b    |
| service_version                   | array\<string> | 17.4mb   | 0.16%     | 6.2mb          | 0b           | 11.1mb     | 0b      | 0b           | 0b    |
| kernel_boot_time                  | double        | 10.2mb   | 0.09%     | 0b             | 0b           | 10.2mb     | 0b      | 0b           | 0b    |
| disk_inodes_used                  | double        | 9.9mb    | 0.09%     | 0b             | 0b           | 9.9mb      | 0b      | 0b           | 0b    |
| disk_inodes_free                  | double        | 9.9mb    | 0.09%     | 0b             | 0b           | 9.9mb      | 0b      | 0b           | 0b    |
| path                              | array\<string> | 6.5mb    | 0.06%     | 1.3mb          | 0b           | 5.1mb      | 0b      | 0b           | 0b    |
| nginx_active                      | double        | 5.3mb    | 0.05%     | 0b             | 0b           | 5.3mb      | 0b      | 0b           | 0b    |
| nginx_reading                     | double        | 5.2mb    | 0.05%     | 0b             | 0b           | 5.2mb      | 0b      | 0b           | 0b    |
| nginx_waiting                     | double        | 5.1mb    | 0.05%     | 0b             | 0b           | 5.1mb      | 0b      | 0b           | 0b    |
| redis_mem_fragmentation_ratio     | double        | 5.0mb    | 0.05%     | 0b             | 0b           | 5.0mb      | 0b      | 0b           | 0b    |
| nginx_writing                     | double        | 5.0mb    | 0.05%     | 0b             | 0b           | 5.0mb      | 0b      | 0b           | 0b    |
| interface                         | array\<string> | 3.9mb    | 0.03%     | 1.1mb          | 0b           | 2.7mb      | 0b      | 0b           | 0b    |
| fstype                            | array\<string> | 3.6mb    | 0.03%     | 959.4kb        | 0b           | 2.6mb      | 0b      | 0b           | 0b    |
| mem_total                         | double        | 2.7mb    | 0.02%     | 0b             | 0b           | 2.7mb      | 0b      | 0b           | 0b    |
| host_ip                           | array\<string> | 2.7mb    | 0.02%     | 2.7mb          | 0b           | 416b       | 0b      | 0b           | 0b    |
| repo                              | string        | 2.7mb    | 0.02%     | 2.7mb          | 0b           | 182b       | 0b      | 0b           | 0b    |
| sourcetype                        | string        | 2.7mb    | 0.02%     | 2.7mb          | 0b           | 182b       | 0b      | 0b           | 0b    |
| disk_used_percent                 | double        | 788.3kb  | 0.01%     | 0b             | 0b           | 788.3kb    | 0b      | 0b           | 0b    |
| disk_total                        | double        | 180.1kb  | 0.00%     | 0b             | 0b           | 180.1kb    | 0b      | 0b           | 0b    |
| disk_inodes_total                 | double        | 180.1kb  | 0.00%     | 0b             | 0b           | 180.1kb    | 0b      | 0b           | 0b    |
| _primary_term                     | unknown       | 0b       | 0.00%     | 0b             | 0b           | 0b         | 0b      | 0b           | 0b    |


tags 字段：占据空间 492.85 MB  百分比 4.43% 
_time 字段   418.2mb / 9 table = 47581 KB   35X (created_at)

usage_user 79.4mb   10X Gorilla 存储空间
usage_system 79.4mb
usage_steal 79.4mb


#### REF

- [一文走进时序数据库性能测试工具 TSBS](https://zhuanlan.zhihu.com/p/649214414)
- [TSBS 是什么？为什么时序数据库 TDengine 会选择它作为性能对比测试平台?](https://zhuanlan.zhihu.com/p/610366672)


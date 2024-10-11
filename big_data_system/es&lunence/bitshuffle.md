# 编码优化

## deltaEncode

ES 对无序的 NumericDocValues 类型，编码默认使用 deltaEncode，块大小 128 * 8B。

即使是float类型，也会转成 long[] 进行编码处理。 

deltaEncode基本思想，缩减值域空间用更少的bits存储，gcd + bit-packing 编码。

该处理方式，特别对于时间戳类型，单调递增的，表现非常好，但是对与float类型压缩很差。

> 参考 ES87TSDBDocValuesFormat 类型的处理， ES87TSDBDocValuesEncoder 具体编码算法


## BitShuffle + lz4 编码

基于 influxdb-comparisons 的 devops测试集(9331 2000行)，BitShuffle + lz4，块大小为4K*8B。


- float 类型的指标，例如cpu_xxx bitshuffle 可以减少了一半的存储空间
- 部分单调递增，或者值域变化不大情况下，例如diskio_read_bytes，net_bytes_recv等，deltaEncode更好，比是BitShuffle进一步减少一半。
- 由于 block size 是128，导致对于string类型的字段，压缩率很低
- 整体压缩情况，BitShuffle + lz4 编码，比deltaEncode 压缩空间可以减少31.6%（1.9GB -> 1.3GB）


（_time字段 都是使用deltaEncode, 写入差异？）

| field                             | devops_total | bitshuffle_devops_total |
| --------------------------------- | ------------ | ----------------------- |
| _tag_names                        | 176182567    | 11618065                |
| _metric_names                     | 167130385    | 13420296                |
| mem_available_percent             | 75563724     | 41914927                |
| mem_used_percent                  | 75501134     | 41902717                |
| mem_buffered_percent              | 75493636     | 41900491                |
| cpu_usage_softirq                 | 75083665     | 40998956                |
| cpu_usage_irq                     | 75083203     | 40990473                |
| cpu_usage_user                    | 75058906     | 40982004                |
| cpu_usage_system                  | 75054593     | 40984764                |
| cpu_usage_guest                   | 75042149     | 40983869                |
| cpu_usage_nice                    | 75038222     | 40979491                |
| cpu_usage_guest_nice              | 75034557     | 40983659                |
| cpu_usage_idle                    | 75033295     | 40987263                |
| cpu_usage_steal                   | 75016339     | 40974582                |
| cpu_usage_iowait                  | 74998578     | 40971650                |
| mem_cached                        | 50060120     | 43372341                |
| mem_available                     | 50007834     | 43366213                |
| mem_free                          | 49936077     | 43361735                |
| mem_buffered                      | 49901962     | 43354728                |
| mem_used                          | 49901962     | 43354728                |
| host                              | 17780780     | 12088596                |
| _time                             | 15925167     | 12810946                |
| rack                              | 15260250     | 11067882                |
| datacenter                        | 12438572     | 9749135                 |
| service                           | 12257270     | 9597297                 |
| redis_instantaneous_output_kbps   | 11982986     | 10066176                |
| redis_instantaneous_ops_per_sec   | 11982236     | 10066650                |
| redis_instantaneous_input_kbps    | 11962562     | 10069196                |
| region                            | 10940767     | 8636174                 |
| team                              | 9108287      | 7308438                 |
| os                                | 8598765      | 6875945                 |
| service_environment               | 8403001      | 6705296                 |
| postgresl_temp_bytes              | 8096215      | 9040673                 |
| diskio_read_bytes                 | 7584428      | 14138986                |
| diskio_write_bytes                | 7584017      | 14126838                |
| diskio_reads                      | 7459712      | 13837197                |
| diskio_writes                     | 7459241      | 13833703                |
| redis_keyspace_misses             | 7454986      | 13840506                |
| redis_keyspace_hits               | 7454499      | 13839080                |
| net_packets_sent                  | 7454283      | 13842981                |
| redis_expired_keys                | 7454070      | 13844765                |
| net_bytes_recv                    | 7454019      | 13835555                |
| net_bytes_sent                    | 7453905      | 13831512                |
| redis_evicted_keys                | 7453653      | 13836109                |
| net_packets_recv                  | 7453459      | 13833188                |
| arch                              | 7206204      | 5732816                 |
| kernel_disk_pages_out             | 7179912      | 12095720                |
| kernel_disk_pages_in              | 7179908      | 12098071                |
| kernel_context_switches           | 7179882      | 12098320                |
| kernel_processes_forked           | 7179866      | 12094449                |
| kernel_interrupts                 | 7179268      | 12097015                |
| diskio_io_time                    | 7171675      | 12087002                |
| diskio_read_time                  | 7171292      | 12082432                |
| diskio_write_time                 | 7171261      | 12087986                |
| redis_total_connections_received  | 7170020      | 12088861                |
| net_drop_in                       | 7169057      | 12089006                |
| net_err_out                       | 7168798      | 12083673                |
| net_err_in                        | 7168393      | 12088950                |
| nginx_requests                    | 7168017      | 12084611                |
| nginx_accepts                     | 7167187      | 12083442                |
| nginx_handled                     | 7166800      | 12084527                |
| net_drop_out                      | 7166179      | 12086026                |
| service_version                   | 7142873      | 5688990                 |
| redis_used_memory_peak            | 6889887      | 13691038                |
| redis_used_memory_rss             | 6889189      | 13695458                |
| redis_used_memory_lua             | 6889139      | 13691555                |
| redis_used_memory                 | 6888975      | 13689897                |
| disk_free                         | 6658381      | 13711815                |
| disk_used                         | 6656795      | 13748894                |
| origin                            | 6486933      | 5635900                 |
| _series                           | 6158066      | 3014337                 |
| server                            | 5464883      | 3717605                 |
| port                              | 5398971      | 3669567                 |
| host_ip                           | 4437334      | 4477419                 |
| sourcetype                        | 4436580      | 4476645                 |
| disk_inodes_free                  | 3321282      | 2198941                 |
| disk_inodes_used                  | 3154417      | 2151543                 |
| serial                            | 3033193      | 2177902                 |
| redis_uptime_in_seconds           | 2993490      | 3175033                 |
| kernel_boot_time                  | 1705023      | 1172240                 |
| redis_connected_clients           | 1576312      | 1210325                 |
| redis_rdb_changes_since_last_save | 1576255      | 1210401                 |
| postgresl_numbackends             | 1556195      | 1170215                 |
| postgresl_tup_deleted             | 1555797      | 1170271                 |
| redis_master_repl_offset          | 1553444      | 1168758                 |
| redis_used_cpu_sys_children       | 1552125      | 1168652                 |
| redis_latest_fork_usec            | 1552104      | 1168772                 |
| redis_repl_backlog_histlen        | 1552068      | 1168613                 |
| postgresl_blks_read               | 1549405      | 1169703                 |
| redis_pubsub_patterns             | 1548716      | 1168653                 |
| redis_used_cpu_user               | 1548185      | 1168697                 |
| postgresl_conflicts               | 1548168      | 1170089                 |
| postgresl_xact_commit             | 1547818      | 1170093                 |
| redis_repl_backlog_active         | 1547130      | 1168606                 |
| redis_sync_partial_err            | 1546925      | 1168851                 |
| redis_connected_slaves            | 1546806      | 1168456                 |
| postgresl_blk_write_time          | 1536705      | 1169892                 |
| path                              | 1531584      | 1293687                 |
| redis_used_cpu_sys                | 1530579      | 1168797                 |
| postgresl_temp_files              | 1530553      | 1169651                 |
| postgresl_tup_fetched             | 1530390      | 1169998                 |
| postgresl_blks_hit                | 1527204      | 1169827                 |
| postgresl_deadlocks               | 1526554      | 1169310                 |
| redis_used_cpu_user_children      | 1526161      | 1168763                 |
| postgresl_tup_returned            | 1525670      | 1169304                 |
| postgresl_tup_inserted            | 1525357      | 1169120                 |
| postgresl_blk_read_time           | 1525179      | 1169107                 |
| postgresl_xact_rollback           | 1525082      | 1169149                 |
| postgresl_tup_updated             | 1524680      | 1169023                 |
| redis_sync_full                   | 1524259      | 1167785                 |
| redis_pubsub_channels             | 1524076      | 1167703                 |
| redis_sync_partial_ok             | 1524006      | 1167576                 |
| redis_repl_backlog_size           | 1523986      | 1167720                 |
| nginx_reading                     | 1493480      | 1035252                 |
| nginx_active                      | 1493383      | 1034388                 |
| mem_total                         | 1485090      | 901857                  |
| nginx_waiting                     | 1471580      | 1035127                 |
| redis_mem_fragmentation_ratio     | 1467214      | 1037917                 |
| nginx_writing                     | 1465099      | 1033951                 |
| interface                         | 1442680      | 1184993                 |
| fstype                            | 1266560      | 1063757                 |
| disk_used_percent                 | 1265704      | 918105                  |
| disk_total                        | 1217465      | 918866                  |
| disk_inodes_total                 | 1217465      | 964498                  |





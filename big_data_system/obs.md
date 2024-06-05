# 可观测性系统

## 存储选型

需求：
- 长文本日志，json,xml等事件
- metric 时序数据
- tracing (列存)，解析后的存储
  - 指标
  - span
  - event
- 动态schema？
  - 入库时，创建的字段

分类
- OLAP 
- 时序数据库 （metric）
- 搜索数据库  （log）
- 共享存储（S3,HDFS）
  - 满足实时性？


### 对比

| 特性/系统                      | apache doris        | starrocks              | databend                                | cnosdb                      | influxdb                      | clickhouse     | opensearch     | [infinity](https://github.com/infiniflow/infinity) |
| -------------------------- | ------------------- | ---------------------- | --------------------------------------- | --------------------------- | ----------------------------- | -------------- | -------------- | -------------------------------------------------- |
| 类型                    | OLAP           | OLAP              | OLAP                               | TSDB                   | TSDB                     | OLAP      | Search    | Search                                        |
| inverted index（日志全文检索）| ✔️             | ✔️                | ✔️（EE版本）                           | ❌<br>日志不支持，metric tag支持| ❌<br>metric tag支持        | ✔️        | ✔️        | ✔️                                            |
| schemaless            | Dynamic Schema |                   |                                    |                        |                          |           | ✔️        |                                               |
| 存储storage size        |                     |                        |                                         |                             |                               |                |                |                                                    |
| 存算分离                  | 分层存储           | ✔️                | ✔️                                 | ✔️                     |                               |                | ❌         |                                                    |
| 分层存储（冷热数据）            | ✔️             |                   |                                    |                        |                               |                | ✔️        |                                                    |
| 云原生                   |                     |                   | ✔️                                 | ✔️                     |                               |                |           |                                                    |
| 写入load time           |                     |                        |                                         |                             |                               |                |                |                                                    |
| 语言                    | 计算java<br>存储C++| 计算java存储C++       | rust                               | rust                   | 2.0 golang<br>3.0 rust   | C++       | java      | C++20                                         |
| 列存                    | ✔️             | ✔️                | ✔️                                 | ✔️                     | ✔️                       | ✔️        | ✔️        |                                                    |
| stream                |                |                   |                                    |                        |                          |           |           |                                                    |
| 向量                    |                     |                        |                                         |                             |                               |                | ✔️        | ✔️                                            |
| license               | Apache-2.0     | Apache-2.0<br>有企业版| Elastic-2.0 +<br>Apache-2.0<br>有企业版| AGPL3.0<br>有企业版        | Apache-2.0<br>MIT<br>有企业版| Apache-2.0| Apache-2.0| Apache-2.0                                    |
| log                   | ✔️             | ✔️                | ❌                                  | ❌                      | ❌                        | ✔️        | ✔️        | ✔️                                            |
| metric                | ✔️             | ✔️                | ✔️                                 | ✔️                     | ✔️                       | ✔️        | ✔️        | ❌                                             |
| tracing               | ✔️             | ✔️                | ✔️                                 | ✔️                     | ❌                        | ✔️        | ✔️        | ❌                                             |
| event                 | ✔️             | ✔️                | ✔️                                 | ✔️                     | ❌                        | ✔️        | ✔️        | ✔️                                            |


## REF
- [ClickBench](https://benchmark.clickhouse.com/)
    - [带你看懂clickbench打榜报告的内容](https://www.cnblogs.com/syw20170419/p/17381314.html) 
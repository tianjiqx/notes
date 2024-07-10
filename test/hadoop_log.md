
# hdfs 日志


## 测试结果

原始： 18 G
扩展字段(常量，时间戳字段)： 26G
行数：8229 3702 rows
（ES 82,292,414 rows）


| 系统         | size（GB）   | load time（s） | 压缩比 | 速度(MB/s) |
| ---------- | ---------- | ------------ | --- | --------- |
| clickhouse（24.6.1.2462,lz4） |  2.46G      |  65.393    |  1.09   |  281.86  |
| doris 2.1.3（lz4）     | 2.263 | 54.248    |  1.0   | 339.77 |
| ES（6.8，zstd-3，无全文索引） | 5.3gb | 1346.581 | 2.34 | 13.69|
| ES（6.8，zstd-1-60k，无全文索引，无source字段） | 4.3gb | 1430.504 | 1.9 | 12.88 |
| ES（6.8，lz4-16k，无全文索引，无source字段） | 5.2gb | 1966.465 | 2.3 | 9.37 |


zstd-3 表示 level 级别在3

ck表：

```
CREATE TABLE logs.test_hdfs
(
    `_time` Int64,
    `_indexTime` Int64,
    `host` FixedString(50),
    `repo` FixedString(50),
    `sourcetype` FixedString(256),
    `origin` FixedString(256),
    `_raw` String
)
ENGINE = MergeTree
PARTITION BY toDate(toDateTime(_time))
PRIMARY KEY _time
ORDER BY _time
SETTINGS index_granularity = 8192

```



### ES 6.8 (lunce 7.7)

#### lz4

5.2 GB

| field         | type           | total   | total_pct | inverted_index | stored_field | doc_values | points  | term_vectors | norms |
|---------------|----------------|---------|-----------|----------------|--------------|------------|---------|--------------|-------|
| _raw          | string         | 2.8gb   | 53.85%    | 0b             | 2.8gb        | 0b         | 0b      | 0b           | 0b    |
| _id           | unknown        | 1.1gb   | 20.49%    | 749.9mb        | 353.4mb      | 0b         | 0b      | 0b           | 0b    |
| _seq_no       | unknown        | 547.9mb | 10.18%    | 0b             | 0b           | 225.4mb    | 322.5mb | 0b           | 0b    |
| _time         | long           | 497.5mb | 9.24%     | 0b             | 0b           | 180.7mb    | 316.8mb | 0b           | 0b    |
| _indexTime    | long           | 326.2mb | 6.06%     | 0b             | 0b           | 167.8mb    | 158.4mb | 0b           | 0b    |
| origin        | string         | 1.9mb   | 0.04%     | 1.9mb          | 0b           | 1.2kb      | 0b      | 0b           | 0b    |
| repo          | string         | 1.9mb   | 0.04%     | 1.9mb          | 0b           | 408b       | 0b      | 0b           | 0b    |
| host_ip       | array\<string> | 1.9mb   | 0.04%     | 1.9mb          | 0b           | 384b       | 0b      | 0b           | 0b    |
| host          | string         | 1.9mb   | 0.04%     | 1.9mb          | 0b           | 312b       | 0b      | 0b           | 0b    |
| sourcetype    | string         | 1.9mb   | 0.04%     | 1.9mb          | 0b           | 192b       | 0b      | 0b           | 0b    |
| _primary_term | unknown        | 0b      | 0.00%     | 0b             | 0b           | 0b         | 0b      | 0b           | 0b    |
| _version      | unknown        | 0b      | 0.00%     | 0b             | 0b           | 0b         | 0b      | 0b           | 0b    |
​

_id, _seq_no 列占据 30% 冗余空间 
_indexTime, _time 15% 

#### zstd1-60k

4.3gb

| field         | type           | total   | total_pct | inverted_index | stored_field | doc_values | points  | term_vectors | norms |
|---------------|----------------|---------|-----------|----------------|--------------|------------|---------|--------------|-------|
| _raw          | string         | 2.0gb   | 46.28%    | 0b             | 2.0gb        | 0b         | 0b      | 0b           | 0b    |
| _id           | unknown        | 994.6mb | 22.50%    | 741.5mb        | 253.1mb      | 0b         | 0b      | 0b           | 0b    |
| _seq_no       | unknown        | 549.3mb | 12.43%    | 0b             | 0b           | 230.4mb    | 318.9mb | 0b           | 0b    |
| _time         | long           | 500.2mb | 11.32%    | 0b             | 0b           | 184.4mb    | 315.9mb | 0b           | 0b    |
| _indexTime    | long           | 320.7mb | 7.25%     | 0b             | 0b           | 161.9mb    | 158.8mb | 0b           | 0b    |
| origin        | string         | 2.0mb   | 0.04%     | 2.0mb          | 0b           | 1.4kb      | 0b      | 0b           | 0b    |
| repo          | string         | 2.0mb   | 0.04%     | 2.0mb          | 0b           | 448b       | 0b      | 0b           | 0b    |
| host_ip       | array\<string> | 2.0mb   | 0.04%     | 2.0mb          | 0b           | 448b       | 0b      | 0b           | 0b    |
| host          | string         | 2.0mb   | 0.04%     | 2.0mb          | 0b           | 364b       | 0b      | 0b           | 0b    |
| sourcetype    | string         | 2.0mb   | 0.04%     | 2.0mb          | 0b           | 224b       | 0b      | 0b           | 0b    |
| _primary_term | unknown        | 0b      | 0.00%     | 0b             | 0b           | 0b         | 0b      | 0b           | 0b    |
| _version      | unknown        | 0b      | 0.00%     | 0b             | 0b           | 0b         | 0b      | 0b           | 0b    |

_id, _seq_no 列占据 34% 冗余空间 
_indexTime, _time 18% 


### zstd3 + source

| field         | type          | total   | total_pct | inverted_index | stored_field | doc_values | points  | term_vectors | norms |
| ------------- | ------------- | ------- | --------- | -------------- | ------------ | ---------- | ------- | ------------ | ----- |
| _raw          | string        | 1.5gb   | 28.98%    | 0b             | 1.5gb        | 0b         | 0b      | 0b           | 0b    |
| _source       | unknown       | 1.5gb   | 28.68%    | 0b             | 1.5gb        | 0b         | 0b      | 0b           | 0b    |
| _id           | unknown       | 927.2mb | 17.19%    | 738.1mb        | 189.1mb      | 0b         | 0b      | 0b           | 0b    |
| _seq_no       | unknown       | 530.7mb | 9.84%     | 0b             | 0b           | 213.4mb    | 317.3mb | 0b           | 0b    |
| _time         | long          | 503.1mb | 9.33%     | 0b             | 0b           | 186.6mb    | 316.5mb | 0b           | 0b    |
| _indexTime    | long          | 310.8mb | 5.76%     | 0b             | 0b           | 152.7mb    | 158.1mb | 0b           | 0b    |
| origin        | string        | 2.3mb   | 0.04%     | 2.3mb          | 0b           | 1.2kb      | 0b      | 0b           | 0b    |
| repo          | string        | 2.3mb   | 0.04%     | 2.3mb          | 0b           | 400b       | 0b      | 0b           | 0b    |
| host_ip       | array\<string> | 2.3mb   | 0.04%     | 2.3mb          | 0b           | 400b       | 0b      | 0b           | 0b    |
| host          | string        | 2.3mb   | 0.04%     | 2.3mb          | 0b           | 325b       | 0b      | 0b           | 0b    |
| sourcetype    | string        | 2.3mb   | 0.04%     | 2.3mb          | 0b           | 200b       | 0b      | 0b           | 0b    |
| _primary_term | unknown       | 0b      | 0.00%     | 0b             | 0b           | 0b         | 0b      | 0b           | 0b    |
| _version      | unknown       | 0b      | 0.00%     | 0b             | 0b           | 0b         | 0b      | 0b           | 0b    |


_source 字段 与 _raw 字段数据重复


#### 结论

ck，doris 对 日志类型数据 比 es 存储空间 更少在于， es 额外辅助结构 _id, _seq_no ，_source 等空间开销， long 时间戳可以进一步优化


## hdfs 测试2

[HDFS_v2](https://zenodo.org/records/8196385/files/HDFS_v2.zip) (17gb)

- clickhouse

load time: 5.59min (不包括 merge time)
disk size: 5gb+ → 2.1gb (12 parts, merge 后)


- lucene 9.11

load time: 6.75min
disk size: 3.4gb (31 segments)


ck 写入峰值是 lucene 的 1.7 倍 (未触发 merge)

lucene 比 ck 存储空间 x1.61


```
{
    "fields": [
        {
            "formats": [
                {
                    "name": "inverted_index",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "stored_field",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "doc_values",
                    "size": "151.2mb",
                    "size_in_bytes": "158592444",
                    "percent": 4.330631732940674
                },
                {
                    "name": "points",
                    "size": "268.9mb",
                    "size_in_bytes": "281958370",
                    "percent": 7.699344158172607
                },
                {
                    "name": "term_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "norms",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "knn_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                }
            ],
            "name": "_time::long",
            "total": "420.1mb",
            "total_in_bytes": "440550814",
            "percent": 12.029976844787598
        },
        {
            "formats": [
                {
                    "name": "inverted_index",
                    "size": "2.0gb",
                    "size_in_bytes": "2164438140",
                    "percent": 59.10360336303711
                },
                {
                    "name": "stored_field",
                    "size": "913.9mb",
                    "size_in_bytes": "958289415",
                    "percent": 26.167694091796875
                },
                {
                    "name": "doc_values",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "points",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "term_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "norms",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "knn_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                }
            ],
            "name": "_raw::text",
            "total": "2.9gb",
            "total_in_bytes": "3122727555",
            "percent": 85.27129364013672
        },
        {
            "formats": [
                {
                    "name": "inverted_index",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "stored_field",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "doc_values",
                    "size": "1.6mb",
                    "size_in_bytes": "1705502",
                    "percent": 0.046571582555770874
                },
                {
                    "name": "points",
                    "size": "3.7mb",
                    "size_in_bytes": "3865313",
                    "percent": 0.10554883629083633
                },
                {
                    "name": "term_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "norms",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "knn_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                }
            ],
            "name": "severityNumber::long",
            "total": "5.3mb",
            "total_in_bytes": "5570815",
            "percent": 0.1521204113960266
        },
        {
            "formats": [
                {
                    "name": "inverted_index",
                    "size": "4.6mb",
                    "size_in_bytes": "4865435",
                    "percent": 0.13285882771015167
                },
                {
                    "name": "stored_field",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "doc_values",
                    "size": "1.6mb",
                    "size_in_bytes": "1683552",
                    "percent": 0.045972201973199844
                },
                {
                    "name": "points",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "term_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "norms",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "knn_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                }
            ],
            "name": "severityText::string",
            "total": "6.2mb",
            "total_in_bytes": "6548987",
            "percent": 0.1788310408592224
        },
        {
            "formats": [
                {
                    "name": "inverted_index",
                    "size": "37.3mb",
                    "size_in_bytes": "39067540",
                    "percent": 1.0668045282363892
                },
                {
                    "name": "stored_field",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "doc_values",
                    "size": "39.8mb",
                    "size_in_bytes": "41738342",
                    "percent": 1.1397351026535034
                },
                {
                    "name": "points",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "term_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "norms",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                },
                {
                    "name": "knn_vectors",
                    "size": "0b",
                    "size_in_bytes": "0",
                    "percent": 0
                }
            ],
            "name": "log.file.name::string",
            "total": "77.1mb",
            "total_in_bytes": "80805882",
            "percent": 2.2065396308898926
        }
    ],
    "total": "3.4gb",
    "total_in_bytes": "3662108729",
    "segments": 31,
    "all_fields": {
        "formats": [
            {
                "name": "inverted_index",
                "size": "2.1gb",
                "size_in_bytes": "2208371115",
                "percent": 60.30326461791992
            },
            {
                "name": "stored_field",
                "size": "913.9mb",
                "size_in_bytes": "958289415",
                "percent": 26.167694091796875
            },
            {
                "name": "doc_values",
                "size": "194.3mb",
                "size_in_bytes": "203719840",
                "percent": 5.562911033630371
            },
            {
                "name": "points",
                "size": "272.6mb",
                "size_in_bytes": "285823683",
                "percent": 7.804893493652344
            },
            {
                "name": "term_vectors",
                "size": "0b",
                "size_in_bytes": "0",
                "percent": 0
            },
            {
                "name": "norms",
                "size": "0b",
                "size_in_bytes": "0",
                "percent": 0
            },
            {
                "name": "knn_vectors",
                "size": "0b",
                "size_in_bytes": "0",
                "percent": 0
            }
        ],
        "name": "",
        "total": "3.4gb",
        "total_in_bytes": "3656204053",
        "percent": 99.83876037597656
    }
}

```

"total": "3.4gb"


按字段：


"name": "_time::long",
"total": "420.1mb",
"percent": 12.029976844787598

"name": "_raw::text",
"total": "2.9gb",
"percent": 85.27129364013672

"name": "severityNumber::long",
"total": "5.3mb",
"percent": 0.1521204113960266

"name": "severityText::string",
"total": "6.2mb",
"percent": 0.1788310408592224

"name": "log.file.name::string",
"total": "77.1mb",
"percent": 2.2065396308898926


分类：

"name": "inverted_index",
"size": "2.1gb",
"percent": 60.30326461791992


"name": "stored_field",
"size": "913.9mb",
"percent": 26.167694091796875


"name": "doc_values",
"size": "194.3mb",
"percent": 5.562911033630371

"name": "points",
"size": "272.6mb",
"percent": 7.804893493652344

总结：
_time 占比 12 % 
inverted_index raw的倒排索引占比 60% 2.1gb



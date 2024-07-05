
# hdfs 日志


## 测试结果

原始： 18 G
扩展字段(常量，时间戳字段)： 26G
行数：8229 3702 rows

| 系统         | size（GB）   | load time（s） | 压缩比 | 速度(MB/s) |
| ---------- | ---------- | ------------ | --- | --------- |
| clickhouse（24.6.1.2462,lz4） |  2.46G      |  65.393    |  1.09   |  281.86  |
| doris 2.1.3（lz4）     | 2.263 | 54.248    |  1.0   | 339.77 |
| ES（6.8，zstd-3，无全文索引） | 5.3gb | 1346.581 | 2.34 | 13.69|
| ES（6.8，zstd-1-60k，无全文索引，无source字段） | 4.3gb | 1430.504 | 1.9 | 12.88 |
| ES（6.8，lz4-16k，无全文索引，无source字段） | 5.2gb | 1966.465 | 2.3 | 9.37 |

（zstd-1 和 zstd-3 不影响空间大小）

### hdfs 测试2

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
inverted_index raw的倒排索引占比2.1gb



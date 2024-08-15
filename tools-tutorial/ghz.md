
# ghz

gRPC基准测试和负载测试工具。


配置和使用

配置文件 spl.toml
```toml
# 总执行次数
total = 10000
# 并发度
concurrency = 10
# host
host = "127.0.0.1:9500"
# 输出文件名
output = "spl_result.html"

# 这些参数固定
insecure = true
# proto 文件服务定义
call = "io.xx.xx.QueryStreamService/Query"
format = "html"

[data]
query = '''xxx'''

[metadata]
Authorization = ""
```

模板变量：

www/docs/calldata.md

- `{"request-id":"{{.RequestNumber}}", "timestamp":"{{.TimestampUnix}}"}`

- 随机数： `host_{{randomInt 0 399}}`


执行：

./ghz --config=spl.toml  

### grpcurl 

grpcurl -plaintext -H "Authorization: $TOKEN" -d '$query' localhost:9500 io.keta.ketadb.QueryStreamService/Query


## REF

- [ghz docs](https://ghz.sh/docs)

- [gRPC 压测工具 ghz_ghz linux 安装](https://blog.csdn.net/blackbattery/article/details/118071611)
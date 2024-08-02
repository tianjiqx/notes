
# OpenDAL
提供了一个统一的数据访问层，使得开发者能够以一致的方式与不同的存储服务（对象存储、文件存储、数据库等）进行交互。OpenDAL 的目标是简化数据访问的复杂性，隐藏掉不同云存储系统之间的差异，从而让开发者可以更专注于业务逻辑而不是底层存储细节。并且提供了Rust中的核心实现以及多语言绑定，如Java，Python和Node.js。

OpenDAL 支持数十种存储服务，覆盖场景全面，支持按需选用：
- 标准存储协议：FTP，HTTP，SFTP，WebDAV 等
- 对象存储服务：azblob，gcs，obs，oss，s3 等
- 文件存储服务：fs, azdfs，hdfs，webhdfs, ipfs 等
- 消费级存储服务（网盘）：Google Drive，OneDrive，Dropbox 等
- Key Value 存储服务：Memory，Redis，Rocksdb 等
- 缓存服务：Ghac，Memcached 等

优势：
- 丰富的存储服务支持
- 多语言跨语言绑定
- 中间件支持
    - 错误重试、可观测性支持、OpenDAL 对所有操作都实现了 logging，tracing，metrics 支持
    - 并发控制，流控，模糊测试等


## 实现

- Operator 负责对用户暴露易用的接口

read API:
op.read(path): 将指定文件全部内容读出
op.reader(path): 创建一个 Reader 用来做流式读取
op.read_with(path).range(1..1024): 使用指定参数来读取文件内容，比如说 range
op.reader_with(path).range(1..1024): 使用指定参数来创建 Reader 做流式读取

- Layers 负责对服务的能力进行补全
    - 通过使用层，我们可以重试失败的请求，并使用RetryLayer从故障点恢复，使用TracingLayer提供本地可观察性等
    - Reader实现 seek
- Services 负责不同服务的具体实现

## 使用

```
// Configure service
final Map<String, String> conf = new HashMap<>();
conf.put("root", "/tmp");
// Construct operator
final Operator op = Operator.of("fs", conf);
// Write data
op.write("hello.txt", "Hello, World!").join();
// Read data
final byte[] bs = op.read("hello.txt").join();
// Delete
op.delete("hello.txt").join();
```


## REF
- [github: apache/opendal](https://github.com/apache/opendal)

- [Apache OpenDAL™ 内部实现：数据读取](https://xuanwo.io/2023/02-how-opendal-read-data/)

- [Apache OpenDAL 毕业随感](https://www.tisonkun.org/2024/01/18/opendal-graduate/)

- [docs/concepts](https://opendal.apache.org/docs/rust/opendal/docs/concepts/index.html)

- [Apache OpenDAL (Incubating) ：无痛数据访问新体验](https://zhuanlan.zhihu.com/p/641548011)

- [OpenDAL/面向 Java 用户的介绍](https://note.xuanwo.io/#/page/opendal%2F%E9%9D%A2%E5%90%91%20java%20%E7%94%A8%E6%88%B7%E7%9A%84%E4%BB%8B%E7%BB%8D)
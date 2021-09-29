## Pebble-笔记

## 1. 简介

Pebble 是一个受 LevelDB/RocksDB 启发的键值存储，供CockroachDB使用。

Pebble 继承了 RocksDB 文件格式，只是完成一些其需要的功能，并增加一些扩展

- 范围删除墓碑
- 表级布隆过滤器
- 对 MANIFEST 格式的更新



特点：

- go 语言实现，用来代替CockroachDB早期使用的RocksDB  （C++）。
  - 基于go 版本的levelDB。

- LSM KV
  - Memtables  + SSTables
    - Memtables 基于并发 Skiplist实现
    - Sstables 在后台定期压缩
- 操作可以分组为原子批次。可以通过 单独读取记录 `Get`，或使用 `Iterator`. 
- 持久化 WAL+ SSTables



## 2.架构原理



## 3. 使用

官方简单例子

```
package main
import (
	"fmt"
	"log"

	"github.com/cockroachdb/pebble"
)
func main() {
	db, err := pebble.Open("demo", &pebble.Options{})
	if err != nil {
		log.Fatal(err)
	}
	key := []byte("hello")
	if err := db.Set(key, []byte("world"), pebble.Sync); err != nil {
		log.Fatal(err)
	}
	value, closer, err := db.Get(key)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s %s\n", key, value)
	if err := closer.Close(); err != nil {
		log.Fatal(err)
	}
	if err := db.Close(); err != nil {
		log.Fatal(err)
	}
}
```

### 3.1 DB基本操作

- `Set` 
  - 设置KV， 会覆盖原key
    - 取出并写入一个`Batch`
    - `DB.Apply()` 应用数据到memtable
      - 并且根据大小，或者是否Sync的参数，作为WAL log flush 到磁盘
    - 执行完成后release  Batch
  - 参数`pebble.Sync` 同步，表示通过操作系统缓冲区缓存将写入同步到实际磁盘。可能导致写入过慢。
    - （考虑，外层提供一个计数器，缓存key，达到固定大小或者，超时后set值，并且要求写wal。避免每次都要wal。并且需要轻量级机制延迟响应客户端）
    - `NewBatch` 可以创建一个只写的batch。
  - `pebble.NoSync` 不同步，进程或计算机崩溃，则可能是最近的写入丢失。
- `Get`
  - `DB.getInternal`
    - `DB.loadReadState`  读引用计数加1，防止文件被删除（GC）
  - 返回值 (value， 迭代器，错误码)
    - `closer.Close()` 读取成功后，需要关闭迭代器，避免内存泄漏（创建的迭代器，从迭代器内存分配器了申请空间，通过close放回）
- `Delete`
  - 同样有Sync或NoSync 参数
  - 先写Batch（delete），然后应用。
  - `DeleteRange` 指定[start,end) 范围删除



- `Close` 关闭DB，非线程安全



- `Flush` 刷 memtable  到磁盘为 SStable
  - `AsyncFlush` 异步
- `Compact` 对一段范围的key 做压缩，合并小文件。

## REF

- [github:pebble](https://github.com/cockroachdb/pebble)
- [Pebble 介绍：一个受 RocksDB 启发的用 Go 编写的键值存储](https://www.cockroachlabs.com/blog/pebble-rocksdb-kv-store/)


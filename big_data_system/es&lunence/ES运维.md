## 1. API 命令

```
// 1. 集群
_cluster/health?pretty
// 节点负载
_cat/nodes?v

// 返回基本索引指标（分片数量、存储大小、内存使用情况）和有关构成集群的当前节点的信息（数量、角色、操作系统、jvm 版本、内存使用情况、cpu 和已安装的插件）
GET /_cluster/stats?human&pretty
GET / _cluster / stats / nodes / node1,node*,master:false 

// 索引，大小降序
GET _cluster/stats/nodes/node1,node*,master:false?pretty"


// 索引恢复
GET /my-index-000001/_recovery?active_only=true&detailed=true
GET /_recovery?human&active_only=true




GET /_cat/indices?v&health=yellow
GET /_cat/indices?v&health=red

GET _cat/indices?v


// 查看集群 unassigned 原因
GET _cluster/allocation/explain?pretty
// 查看指定索引 shard的分配失败原因
curl -X GET "localhost:9200/_cluster/allocation/explain?pretty" -H 'Content-Type: application/json' -d'
{
  "index": "my-index-000001", 
  "shard": 0, 
  "primary": true 
}
'


// 分片
// 名字降序
_cat/shards?v&s=index:desc


// UNASSIGNED 原因
_cat/shards?h=index,shard,prirep,state,unassigned.reason | grep UNASSIGNED

// 找到分配失败的分片
curl -XGET  ${eshost}/_cat/shards?h=index,shard,prirep,state,unassigned.reason,ud -H 'Content-Type: application/json' -H "Authorization: $tk"

// 通过nodes接口查询node信息，并且通过节点id找到对应节点
curl -X GET  ${eshost}/_nodes?pretty -H 'Content-Type: application/json' -H "Authorization: $tk"

// 常见处理：
// 1. 检查 cluster.routing.allocation.enable 是否禁止了分片
// 2. 磁盘损坏，丢失数据，手动创建空shard
curl -X POST 'https://loclhost.com:9200/_cluster/reroute?pretty'-H 'Content-Type: application/json' -d'
{
  "commands": [
     {
         "allocate_empty_primary" : {
            "index" : "xxx
            "shard" :17,
            "node" : "xs4018_1",
            "accept_data_loss" : true
        }
     }   
  ]
}
'
// 3. 重试，分配失败
curl -XPOST <ip>:<port>/_cluster/reroute?retry_failed=true 
curl -XGET http://localhost:9200/_cluster/allocation/explain


# 查看指定索引的分配失败原因
curl -X GET "localhost:9200/api/v1/admin/internal/_cluster/allocation/explain?pretty" -H 'Content-Type: application/json' -d'
{
  "index": "my-index-000001", 
  "shard": 0, 
  "primary": true 
}
'
// 查看，写分片路径path字段，文档数
_cat/write_shards?v&bytes=b

// 手动迁移shard到别的节点，处理 read only
POST _cluster/reroute
{
  "commands": [
    {
      "move": {
        "index": "index_name",
        "shard": 0,
        "from_node": "hostname-a",
        "to_node": "hostname-b"
      }
    }
  ]
}


// 4. 检查磁盘水位
curl -s 'localhost:9200/_cat/allocation?v'


// 返回有关正在进行和已完成的分片恢复的信息（恢复任务数，进度）
/_cat/recovery?active_only&v=true



// tasks
GET /_tasks/<task_id>
GET /_tasks?pretty

curl -X GET "localhost:9200/_tasks?pretty"
curl -X GET "localhost:9200/_tasks?nodes=nodeId1,nodeId2&pretty"
curl -X GET "localhost:9200/_tasks?nodes=nodeId1,nodeId2&actions=cluster:*&pretty"

curl -X GET "localhost:9200/_tasks/oTUltX4IQMOUUVeiohTt8A:124?pretty"
curl -X GET "localhost:9200/_tasks?parent_task_id=oTUltX4IQMOUUVeiohTt8A:123&pretty"




// 查看搜索任务
curl -X GET "localhost:9200/_tasks?actions=*search&detailed&pretty"

curl -X GET "localhost:9200/_tasks?group_by=parents&pretty"

// 取消任务
curl -X POST "localhost:9200/_tasks/oTUltX4IQMOUUVeiohTt8A:12345/_cancel?pretty"


// setting
GET /_cluster/settings?pretty

GET /*/_settings?pretty

GET /my-index-000001/_settings?pretty


// mapping
GET /my-index-000001/_mapping?pretty

/api/v1/admin/internal/<index_name>/_mapping?pretty


// 线程
GET /_cat/thread_pool/<thread_pool>
GET /_cat/thread_pool

_cat/thread_pool?v&h=node_name,name,type,active,queue,rejected,completed,size,queue_size,largest,min,max,keep_alive,pid,ip,port,ephemeral_node_id,host


// 查看写线程状态，活跃数据量，完成任务数
_cat/thread_pool/write?v=true&h=node_name,name,active,queue,rejected,completed

// 查看节点热点线程
GET /_nodes/hot_threads?threads=5&interval=500ms
GET /_nodes/nodeId1,nodeId2/hot_threads

// 节点下线
PUT /_cluster/settings
{
  "transient": {
    "cluster.routing.allocation.exclude._ip": "122.5.3.55"
  }
}


// 滚动重启
// 1.可能的话，停止索引新的数据。虽然不是每次都能真的做到，但是这一步可以帮助提高恢复速度。
// 2.禁止分片分配。这一步阻止 Elasticsearch 再平衡缺失的分片。
PUT /_cluster/settings
{
    "transient" : {
        "cluster.routing.allocation.enable" : "none"
    }
}
// 3.关闭单个节点。
// 4.执行维护/升级。
// 5.重启节点，然后确认它加入到集群了。
// 6.用如下命令重启分片分配：
PUT /_cluster/settings
{
    "transient" : {
        "cluster.routing.allocation.enable" : "all"
    }
}
// 分片再平衡会花一些时间。一直等到集群变成 绿色 状态后再继续。
// 7.重复第 2 到 6 步操作剩余节点。
// 8.恢复索引数据。
```

## 2.常见问题处理
### ES 节点 磁盘 高水位，导致节点上的索引 read_only / delete 状态

- 当集群磁盘使用率超过85%低警戒水位线：会导致新的分片无法分配。
- 当集群磁盘使用率超过90%高警戒水位线：Elasticsearch 会尝试将对应节点中的分片迁移到其他磁盘使用率比较低的数据节点中。
- 当集群磁盘使用率超过95%洪泛警戒水位线：系统会对 Elasticsearch 集群中对应节点里每个索引强制设置 read_only_allow_delete 属性，此时该节点上的所有索引将无法写入数据，只能读取和删除对应索引。


处理：
- 清理集群过期/旧数据 （如果允许）// 扩展磁盘空间 // 什么都不做等待分片迁移，负载均衡 // 调整水位（爆盘风险）
- 关闭索引只读状态， 关闭集群只读状态
```
PUT _all/_settings
{
         "index.blocks.read_only_allow_delete": null
}
PUT _cluster/settings
{
         "persistent": {
             "cluster.blocks.read_only_allow_delete": null
         }
}

```
- 调整写索引并发（可能应该调小），主动rollover, 负载均衡写分片，包括配置禁止在高水位节点，分配分片

```
curl -X PUT  index/_settings -H 'Content-Type: application/json'  -d '{
        "index.routing.allocation.exclude._name" : "node_*"
}'
```


#### REF
- [集群磁盘使用率高和 read_only 状态问题如何解决？ - 腾讯云](https://cloud.tencent.com/document/product/845/56276)
- [Elasticsearch 磁盘使用率超过警戒水位线，怎么办？ - 腾讯云](https://cloud.tencent.com/developer/article/1941253)



### REF

- [rest-apis](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)

- [彻底解决 es 的 unassigned shards 症状](https://toutiao.io/posts/na8zgp/preview)
  
  - 检查 cluster.routing.allocation.enable 是否禁止了分片

- [索引某个shard无法恢复的问题](https://elasticsearch.cn/question/3998) failed to obtain in-memory shard lock
  
  - /_cluster/reroute?retry_failed=true 依然失败
  - 重启一下该节点
  - [es实战-分片分配失败解决方案](https://developer.aliyun.com/article/789498)

- [干货 | Elasticsearch 运维实战常用命令清单](https://mp.weixin.qq.com/s?__biz=MzI2NDY1MTA3OQ==&mid=2247485141&idx=1&sn=c785d6c128761c33f9744bf1454a472a)

- [Elasitcsearch 开发运维常用命令集锦](https://mp.weixin.qq.com/s?__biz=MzI2NDY1MTA3OQ==&mid=2247487406&idx=1&sn=7f4d62b2710af7a833a66371c873d8af)

- [Diagnose unassigned shards](https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnose-unassigned-shards.html)


- [Elasticsearch常用的命令](https://armsword.com/2022/09/27/the-most-frequently-used-commands-of-elasticsearch/) 命令丰富
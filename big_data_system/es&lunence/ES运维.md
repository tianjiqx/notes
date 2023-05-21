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


// 查看集群 unassigned 原因
GET _cluster/allocation/explain?pretty

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

// 查看写线程状态，活跃数据量，完成任务数
_cat/thread_pool/write?v=true&h=node_name,name,active,queue,rejected,completed


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

### REF

- [rest-apis](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)

- [彻底解决 es 的 unassigned shards 症状](https://toutiao.io/posts/na8zgp/preview)
  
  - 检查 cluster.routing.allocation.enable 是否禁止了分片

- [索引某个shard无法恢复的问题](https://elasticsearch.cn/question/3998) failed to obtain in-memory shard lock
  
  - /_cluster/reroute?retry_failed=true 依然失败
  - 重启一下该节点

- [干货 | Elasticsearch 运维实战常用命令清单](https://mp.weixin.qq.com/s?__biz=MzI2NDY1MTA3OQ==&mid=2247485141&idx=1&sn=c785d6c128761c33f9744bf1454a472a)

- [Elasitcsearch 开发运维常用命令集锦](https://mp.weixin.qq.com/s?__biz=MzI2NDY1MTA3OQ==&mid=2247487406&idx=1&sn=7f4d62b2710af7a833a66371c873d8af)

- https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnose-unassigned-shards.html

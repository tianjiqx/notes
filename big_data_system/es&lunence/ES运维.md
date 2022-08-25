

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
GET /_recovery

GET /_cat/indices?v&health=yellow
GET /_cat/indices?v&health=red


// 查看集群 unassigned 原因
GET _cluster/allocation/explain


// 分片
// 名字降序
_cat/shards?v&s=index:desc"
// UNASSIGNED 原因
_cat/shards?h=index,shard,prirep,state,unassigned.reason | grep UNASSIGNED

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


// mapping
GET /my-index-000001/_mapping?pretty

/api/v1/admin/internal/<index_name>/_mapping?pretty


// 线程
GET /_cat/thread_pool/<thread_pool>
GET /_cat/thread_pool

// 查看写线程状态，活跃数据量，完成任务数
_cat/thread_pool/write?v=true&h=h=node_name,name,active,queue,rejected,completed


// 节点下线
PUT /_cluster/settings
{
  "transient": {
    "cluster.routing.allocation.exclude._ip": "122.5.3.55"
  }
}

```



### REF

- [rest-apis](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)
- 
- [干货 | Elasticsearch 运维实战常用命令清单](https://mp.weixin.qq.com/s?__biz=MzI2NDY1MTA3OQ==&mid=2247485141&idx=1&sn=c785d6c128761c33f9744bf1454a472a)
- [Elasitcsearch 开发运维常用命令集锦](https://mp.weixin.qq.com/s?__biz=MzI2NDY1MTA3OQ==&mid=2247487406&idx=1&sn=7f4d62b2710af7a833a66371c873d8af)


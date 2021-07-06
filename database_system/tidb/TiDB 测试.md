# TiDB 测试

### 编译成功后，运行

```shell
nohup ./bin/tidb-server  > 1.log 2>&1 &
mysql -h 127.0.0.1 -P 4000 -u root -D test --prompt="tidb> " 
```



### 建表

```sql
create table t1(c1 int primary key,c2 int,c3 int);
create table t2(c1 int primary key,c2 int,c3 int);
create table t3(c1 int primary key,c2 int,c3 int);
create table t4(c1 int primary key,c2 int,c3 int);
create table t5(c1 int primary key,c2 int,c3 int);


insert into t1 values(1,1,2);
insert into t1 values(2,2,4);
insert into t1 values(3,3,2);
insert into t1 values(4,4,4);
insert into t1 values(5,5,2);


insert into t2 values(1,1,2);
insert into t2 values(2,2,4);
insert into t2 values(3,3,2);
insert into t2 values(4,4,4);


insert into t3 values(1,1,2);
insert into t3 values(2,2,4);
insert into t3 values(3,3,2);


insert into t4 values(1,1,2);
insert into t4 values(2,2,4);
insert into t4 values(3,3,2);
insert into t4 values(4,4,4);

insert into t5 values(1,1,2);
insert into t5 values(2,2,4);
insert into t5 values(3,null,2);
insert into t5 values(4,null,4);
insert into t5 values(5,null,4);
```



### 参数

```sql
-- 显示会话变量，是否开启级联优化器
show variables like 'tidb_enable_cascades_planner';
```

在线修改 TiDB Server的日志级别

```
curl -X POST -d "log_level=trace" http://127.0.0.1:10080/settings
curl -X POST -d "log_level=info" http://127.0.0.1:10080/settings
```



more:[tidb_http_api](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)



### 外连接消除测试

```sql
explain select t1.c1,t2.c1,t3.c1 from  t1 left join t2 on t1.c1=t2.c2 left join t3 on t2.c1=t3.c2 where t3.c3< 5; 

-- v5.1 确实已经可以进行级联的外连接消除了
tidb> explain select t1.c1,t2.c1,t3.c1 from  t1 left join t2 on t1.c1=t2.c2 left join t3 on t2.c1=t3.c2 where t3.c3< 5; 
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| id                                 | estRows | task      | access object | operator info                                                                                                       |
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| Projection_12                      | 1.56    | root      |               | test.t1.c1, test.t2.c1, test.t3.c1                                                                                  |
| └─IndexJoin_17                     | 1.56    | root      |               | inner join, inner:TableReader_14, outer key:test.t2.c2, inner key:test.t1.c1, equal cond:eq(test.t2.c2, test.t1.c1) |
|   ├─IndexJoin_30(Build)            | 1.25    | root      |               | inner join, inner:TableReader_26, outer key:test.t3.c2, inner key:test.t2.c1, equal cond:eq(test.t3.c2, test.t2.c1) |
|   │ ├─TableReader_39(Build)        | 1.00    | root      |               | data:Selection_38                                                                                                   |
|   │ │ └─Selection_38               | 1.00    | cop[tikv] |               | lt(test.t3.c3, 5), not(isnull(test.t3.c2))                                                                          |
|   │ │   └─TableFullScan_37         | 3.00    | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                      |
|   │ └─TableReader_26(Probe)        | 1.00    | root      |               | data:Selection_25                                                                                                   |
|   │   └─Selection_25               | 1.00    | cop[tikv] |               | not(isnull(test.t2.c1)), not(isnull(test.t2.c2))                                                                    |
|   │     └─TableRangeScan_24        | 1.00    | cop[tikv] | table:t2      | range: decided by [test.t3.c2], keep order:false, stats:pseudo                                                      |
|   └─TableReader_14(Probe)          | 1.00    | root      |               | data:TableRangeScan_13                                                                                              |
|     └─TableRangeScan_13            | 1.00    | cop[tikv] | table:t1      | range: decided by [test.t2.c2], keep order:false, stats:pseudo                                                      |
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
11 rows in set (0.00 sec)


-- 开启级联优化器
set @@tidb_enable_cascades_planner=on;
tidb> explain select t1.c1,t2.c1,t3.c1 from  t1 left join t2 on t1.c1=t2.c2 left join t3 on t2.c1=t3.c2 where t3.c3< 5;
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------+
| id                                 | estRows | task      | access object | operator info                                                             |
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------+
| Projection_27                      | 4.00    | root      |               | test.t1.c1, test.t2.c1, test.t3.c1                                        |
| └─Selection_28                     | 4.00    | root      |               | lt(test.t3.c3, 5)                                                         |
|   └─HashJoin_30                    | 5.00    | root      |               | left outer join, equal:[eq(test.t2.c1, test.t3.c2)]                       |
|     ├─TableReader_38(Build)        | 2.40    | root      |               | data:Selection_39                                                         |
|     │ └─Selection_39               | 2.40    | cop[tikv] |               | not(isnull(test.t3.c2)), not(isnull(test.t3.c2)), not(isnull(test.t3.c2)) |
|     │   └─TableFullScan_40         | 3.00    | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                            |
|     └─HashJoin_32(Probe)           | 5.00    | root      |               | left outer join, equal:[eq(test.t1.c1, test.t2.c2)]                       |
|       ├─TableReader_35(Build)      | 3.20    | root      |               | data:Selection_36                                                         |
|       │ └─Selection_36             | 3.20    | cop[tikv] |               | not(isnull(test.t2.c2))                                                   |
|       │   └─TableFullScan_37       | 4.00    | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                            |
|       └─TableReader_33(Probe)      | 5.00    | root      |               | data:TableFullScan_34                                                     |
|         └─TableFullScan_34         | 5.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                            |
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------+
12 rows in set (0.01 sec)


-- 决策的计划不一样，并且似乎完全未优化？， 没有下推，没有外连接消除，优化的时间看起来也更长。




trace format='row' explain select t1.c1,t2.c1,t3.c1 from  t1 left join t2 on t1.c1=t2.c2 left join t3 on t2.c1=t3.c2 where t3.c3< 5;



```



### 多表连接测试

```sql
-- 1)链式连接， 头表有过滤条件
select t1.c1,t2.c1,t3.c1,t4.c1,t5.c1 from t1 inner join t2 on t1.c1=t2.c2 inner join t3 on t2.c1=t3.c2 inner join t4 on t3.c1=t4.c2 inner join t5 on t4.c1=t5.c2 where t1.c3 < 5;

-- 2)链式连接， 中间表有过滤条件
select t1.c1,t2.c1,t3.c1,t4.c1,t5.c1 from t1 inner join t2 on t1.c1=t2.c2 inner join t3 on t2.c1=t3.c2 inner join t4 on t3.c1=t4.c2 inner join t5 on t4.c1=t5.c2 where t3.c3 < 5;

-- 3)链式连接， 尾表有过滤条件
select t1.c1,t2.c1,t3.c1,t4.c1,t5.c1 from t1 inner join t2 on t1.c1=t2.c2 inner join t3 on t2.c1=t3.c2 inner join t4 on t3.c1=t4.c2 inner join t5 on t4.c1=t5.c2 where t5.c3 < 5;

--  测试结果
-- 1) t1表构建桶，t2探测，结果再构建hash桶，t3探测,重复。 连接顺序未变。符合预期
tidb> explain select t1.c1,t2.c1,t3.c1,t4.c1,t5.c1 from t1 inner join t2 on t1.c1=t2.c2 inner join t3 on t2.c1=t3.c2 inner join t4 on t3.c1=t4.c2 inner join t5 on t4.c1=t5.c2 where t1.c3 < 5;
+------------------------------------------+---------+-----------+---------------+------------------------------------------------+
| id                                       | estRows | task      | access object | operator info                                  |
+------------------------------------------+---------+-----------+---------------+------------------------------------------------+
| HashJoin_22                              | 4.06    | root      |               | inner join, equal:[eq(test.t4.c1, test.t5.c2)] |
| ├─HashJoin_24(Build)                     | 3.25    | root      |               | inner join, equal:[eq(test.t3.c1, test.t4.c2)] |
| │ ├─HashJoin_26(Build)                   | 2.60    | root      |               | inner join, equal:[eq(test.t2.c1, test.t3.c2)] |
| │ │ ├─HashJoin_39(Build)                 | 2.08    | root      |               | inner join, equal:[eq(test.t1.c1, test.t2.c2)] |
| │ │ │ ├─TableReader_45(Build)            | 1.66    | root      |               | data:Selection_44                              |
| │ │ │ │ └─Selection_44                   | 1.66    | cop[tikv] |               | lt(test.t1.c3, 5)                              |
| │ │ │ │   └─TableFullScan_43             | 5.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo                 |
| │ │ │ └─TableReader_42(Probe)            | 4.00    | root      |               | data:Selection_41                              |
| │ │ │   └─Selection_41                   | 4.00    | cop[tikv] |               | not(isnull(test.t2.c2))                        |
| │ │ │     └─TableFullScan_40             | 4.00    | cop[tikv] | table:t2      | keep order:false, stats:pseudo                 |
| │ │ └─TableReader_48(Probe)              | 3.00    | root      |               | data:Selection_47                              |
| │ │   └─Selection_47                     | 3.00    | cop[tikv] |               | not(isnull(test.t3.c2))                        |
| │ │     └─TableFullScan_46               | 3.00    | cop[tikv] | table:t3      | keep order:false, stats:pseudo                 |
| │ └─TableReader_51(Probe)                | 4.00    | root      |               | data:Selection_50                              |
| │   └─Selection_50                       | 4.00    | cop[tikv] |               | not(isnull(test.t4.c2))                        |
| │     └─TableFullScan_49                 | 4.00    | cop[tikv] | table:t4      | keep order:false, stats:pseudo                 |
| └─TableReader_54(Probe)                  | 5.00    | root      |               | data:Selection_53                              |
|   └─Selection_53                         | 5.00    | cop[tikv] |               | not(isnull(test.t5.c2))                        |
|     └─TableFullScan_52                   | 5.00    | cop[tikv] | table:t5      | keep order:false, stats:pseudo                 |
+------------------------------------------+---------+-----------+---------------+------------------------------------------------+
19 rows in set (0.00 sec)

-- 2) t3 和 t2 先做index join，t2表探测，然后依次和t4,t5 做hash join，最后和t1 做index join。计划也较好。
tidb> explain select t1.c1,t2.c1,t3.c1,t4.c1,t5.c1 from t1 inner join t2 on t1.c1=t2.c2 inner join t3 on t2.c1=t3.c2 inner join t4 on t3.c1=t4.c2 inner join t5 on t4.c1=t5.c2 where t3.c3 < 5;
+--------------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| id                                         | estRows | task      | access object | operator info                                                                                                       |
+--------------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| Projection_25                              | 2.43    | root      |               | test.t1.c1, test.t2.c1, test.t3.c1, test.t4.c1, test.t5.c1                                                          |
| └─IndexJoin_30                             | 2.43    | root      |               | inner join, inner:TableReader_27, outer key:test.t2.c2, inner key:test.t1.c1, equal cond:eq(test.t2.c2, test.t1.c1) |
|   ├─HashJoin_38(Build)                     | 1.95    | root      |               | inner join, equal:[eq(test.t4.c1, test.t5.c2)]                                                                      |
|   │ ├─HashJoin_40(Build)                   | 1.56    | root      |               | inner join, equal:[eq(test.t3.c1, test.t4.c2)]                                                                      |
|   │ │ ├─IndexJoin_47(Build)                | 1.25    | root      |               | inner join, inner:TableReader_43, outer key:test.t3.c2, inner key:test.t2.c1, equal cond:eq(test.t3.c2, test.t2.c1) |
|   │ │ │ ├─TableReader_56(Build)            | 1.00    | root      |               | data:Selection_55                                                                                                   |
|   │ │ │ │ └─Selection_55                   | 1.00    | cop[tikv] |               | lt(test.t3.c3, 5), not(isnull(test.t3.c2))                                                                          |
|   │ │ │ │   └─TableFullScan_54             | 3.00    | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                      |
|   │ │ │ └─TableReader_43(Probe)            | 1.00    | root      |               | data:Selection_42                                                                                                   |
|   │ │ │   └─Selection_42                   | 1.00    | cop[tikv] |               | not(isnull(test.t2.c2))                                                                                             |
|   │ │ │     └─TableRangeScan_41            | 1.00    | cop[tikv] | table:t2      | range: decided by [test.t3.c2], keep order:false, stats:pseudo                                                      |
|   │ │ └─TableReader_62(Probe)              | 4.00    | root      |               | data:Selection_61                                                                                                   |
|   │ │   └─Selection_61                     | 4.00    | cop[tikv] |               | not(isnull(test.t4.c2))                                                                                             |
|   │ │     └─TableFullScan_60               | 4.00    | cop[tikv] | table:t4      | keep order:false, stats:pseudo                                                                                      |
|   │ └─TableReader_65(Probe)                | 5.00    | root      |               | data:Selection_64                                                                                                   |
|   │   └─Selection_64                       | 5.00    | cop[tikv] |               | not(isnull(test.t5.c2))                                                                                             |
|   │     └─TableFullScan_63                 | 5.00    | cop[tikv] | table:t5      | keep order:false, stats:pseudo                                                                                      |
|   └─TableReader_27(Probe)                  | 1.00    | root      |               | data:TableRangeScan_26                                                                                              |
|     └─TableRangeScan_26                    | 1.00    | cop[tikv] | table:t1      | range: decided by [test.t2.c2], keep order:false, stats:pseudo                                                      |
+--------------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
19 rows in set (0.01 sec)

-- 3) 全是index join，t5 开始，依次和t4,t3,t2,t1 探测连接
tidb> explain select t1.c1,t2.c1,t3.c1,t4.c1,t5.c1 from t1 inner join t2 on t1.c1=t2.c2 inner join t3 on t2.c1=t3.c2 inner join t4 on t3.c1=t4.c2 inner join t5 on t4.c1=t5.c2 where t5.c3 < 5;
+--------------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| id                                         | estRows | task      | access object | operator info                                                                                                       |
+--------------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| Projection_22                              | 4.05    | root      |               | test.t1.c1, test.t2.c1, test.t3.c1, test.t4.c1, test.t5.c1                                                          |
| └─IndexJoin_27                             | 4.05    | root      |               | inner join, inner:TableReader_24, outer key:test.t2.c2, inner key:test.t1.c1, equal cond:eq(test.t2.c2, test.t1.c1) |
|   ├─IndexJoin_40(Build)                    | 3.24    | root      |               | inner join, inner:TableReader_36, outer key:test.t3.c2, inner key:test.t2.c1, equal cond:eq(test.t3.c2, test.t2.c1) |
|   │ ├─IndexJoin_53(Build)                  | 2.59    | root      |               | inner join, inner:TableReader_49, outer key:test.t4.c2, inner key:test.t3.c1, equal cond:eq(test.t4.c2, test.t3.c1) |
|   │ │ ├─IndexJoin_66(Build)                | 2.08    | root      |               | inner join, inner:TableReader_62, outer key:test.t5.c2, inner key:test.t4.c1, equal cond:eq(test.t5.c2, test.t4.c1) |
|   │ │ │ ├─TableReader_75(Build)            | 1.66    | root      |               | data:Selection_74                                                                                                   |
|   │ │ │ │ └─Selection_74                   | 1.66    | cop[tikv] |               | lt(test.t5.c3, 5), not(isnull(test.t5.c2))                                                                          |
|   │ │ │ │   └─TableFullScan_73             | 5.00    | cop[tikv] | table:t5      | keep order:false, stats:pseudo                                                                                      |
|   │ │ │ └─TableReader_62(Probe)            | 1.00    | root      |               | data:Selection_61                                                                                                   |
|   │ │ │   └─Selection_61                   | 1.00    | cop[tikv] |               | not(isnull(test.t4.c2))                                                                                             |
|   │ │ │     └─TableRangeScan_60            | 1.00    | cop[tikv] | table:t4      | range: decided by [test.t5.c2], keep order:false, stats:pseudo                                                      |
|   │ │ └─TableReader_49(Probe)              | 1.00    | root      |               | data:Selection_48                                                                                                   |
|   │ │   └─Selection_48                     | 1.00    | cop[tikv] |               | not(isnull(test.t3.c2))                                                                                             |
|   │ │     └─TableRangeScan_47              | 1.00    | cop[tikv] | table:t3      | range: decided by [test.t4.c2], keep order:false, stats:pseudo                                                      |
|   │ └─TableReader_36(Probe)                | 1.00    | root      |               | data:Selection_35                                                                                                   |
|   │   └─Selection_35                       | 1.00    | cop[tikv] |               | not(isnull(test.t2.c2))                                                                                             |
|   │     └─TableRangeScan_34                | 1.00    | cop[tikv] | table:t2      | range: decided by [test.t3.c2], keep order:false, stats:pseudo                                                      |
|   └─TableReader_24(Probe)                  | 1.00    | root      |               | data:TableRangeScan_23                                                                                              |
|     └─TableRangeScan_23                    | 1.00    | cop[tikv] | table:t1      | range: decided by [test.t2.c2], keep order:false, stats:pseudo                                                      |
+--------------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
19 rows in set (0.01 sec)


```



### 断点调试

```
// SQL:
explain select t1.c1,t2.c1,t3.c1 from  t1 left join t2 on t1.c1=t2.c2 left join t3 on t2.c1=t3.c2 where t2.c3< 5;

// 添加断点，逻辑优化结束
b planner/core/optimizer.go:148

// 添加断点， logicalplan
b planner/core/find_best_task.go:287

// 添加断点， datasource
b planner/core/find_best_task.go:617 
// p p.children[0].tableInfo

// 添加断点，logical join转物理join计划 穷举
b planner/core/exhaust_physical_plans.go:1692

tidb> explain select t1.c1,t2.c1,t3.c1 from  t1 left join t2 on t1.c1=t2.c2 left join t3 on t2.c1=t3.c2 where t3.c3< 5;
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| id                                 | estRows | task      | access object | operator info                                                                                                       |
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
| Projection_12                      | 1.56    | root      |               | test.t1.c1, test.t2.c1, test.t3.c1                                                                                  |
| └─IndexJoin_17                     | 1.56    | root      |               | inner join, inner:TableReader_14, outer key:test.t2.c2, inner key:test.t1.c1, equal cond:eq(test.t2.c2, test.t1.c1) |
|   ├─IndexJoin_30(Build)            | 1.25    | root      |               | inner join, inner:TableReader_26, outer key:test.t3.c2, inner key:test.t2.c1, equal cond:eq(test.t3.c2, test.t2.c1) |
|   │ ├─TableReader_39(Build)        | 1.00    | root      |               | data:Selection_38                                                                                                   |
|   │ │ └─Selection_38               | 1.00    | cop[tikv] |               | lt(test.t3.c3, 5), not(isnull(test.t3.c2))                                                                          |
|   │ │   └─TableFullScan_37         | 3.00    | cop[tikv] | table:t3      | keep order:false, stats:pseudo                                                                                      |
|   │ └─TableReader_26(Probe)        | 1.00    | root      |               | data:Selection_25                                                                                                   |
|   │   └─Selection_25               | 1.00    | cop[tikv] |               | not(isnull(test.t2.c1)), not(isnull(test.t2.c2))                                                                    |
|   │     └─TableRangeScan_24        | 1.00    | cop[tikv] | table:t2      | range: decided by [test.t3.c2], keep order:false, stats:pseudo                                                      |
|   └─TableReader_14(Probe)          | 1.00    | root      |               | data:TableRangeScan_13                                                                                              |
|     └─TableRangeScan_13            | 1.00    | cop[tikv] | table:t1      | range: decided by [test.t2.c2], keep order:false, stats:pseudo                                                      |
+------------------------------------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------+
11 rows in set (0.01 sec)


// 物理计划的探索，递归logical plan 转 physical plan，先最外层的LogicalProjection(Projection_12)算子，然后孩子节点LogicalJoin，这个孩子节点有两个子孩子，LogicalJoin(t2,t3)和DataSource(t1)。 枚举连接算法，计算最小代价。

```







Tidb2.1的TopN下压
----

### 问题描述：

所谓TopN下压是指将SQL中的top子句下压到更底层的位置执行，原始top子句的顺序是在整个sql最后执行（join子句，where子句等完成后）。TopN下压和其他的下压操作如谓词下压，聚集函数下压等操作都是为了提前完成数据的过滤，减少后续算子处理的数据量，加快查询执行。带有topn子句的例子`select top 10 * from t1;`。

另外，limit子句也是topn的一种，在tidb中通过`LogicalLimit`的`convertToTopN()`方法将limit转化为TopN的逻辑计划节点结构后下压。

### 相关文件与结构说明：

TopN下压的所有的相关代码都在`tidb/plan/rule_topn_push_down.go`文件中 。

##### 数据结构与方法：
- `pushDownTopNOptimizer`:
	TopN下压优化器，只有一个optimize()方法，并无实质内容，仅调用传入的逻辑计划节点的`pushDownTopN`方法。

- `LogicalTopN`:
	TopN子句对应的LogicalPlan节点，其主要成员有继承一个基类的LogicalPlan的struct类。型。`baseLogicalPlan`；`ByItems []*ByItems`是TopN子句所在的子查询的group/order by子句涉及的列，用于TopN检测是否可以下压；`Offset  uint64`和`Count   uint64`是偏移和取TOP值。

- `baseLogicalPlan.pushDownTopN()`：
	LogicalPlan节点基类的TopN下压方法，子类的默认继承了该方法。该方法是会调用其子孩子的`pushDownTopN()`方法，完成TopN下压的自顶向下传递。

- `LogicalUnionAll、LogicalLimit、LogicalSort、LogicalProjection、LogicalJoin`：
	这几个LogicalPlan结构，重写了`baseLogicalPlan`的`pushDownTopN`方法，在TopN子句自顶向下下压的过程中，做下压或调整后下压LogicalTopN对象。
	
### 实现：
- union all：重新构造LogicalTopN对象，下压到LogicalUnionAll的孩子节点。新LogicalTopN的Count为原始的count+offset，offset=0，ByItems不变。
- limit：通过limit子句设置 LogicalTopN的offset和count
- sort：当下压成功能时，去掉sort逻辑计划
- project：下压到project下面时需要重新替换一下LogicalTopN中by列的列名
- join：如果LogicalTopN的by列只包含join的一个孩子，则可以下压到包含by列的孩子节点，否则停止下压。

	
### 举例说明：

例，`select top 10 * from t1 left join t2 on t1.c1=t2.c2 order by t1.c2;`可以重写下推为如下形式`select * from (select * from t1 order by t1.c2 limit 10) a left join t2 on a.c1=t2.c2 order by t1.c2 limit 10;`。

原SQL中需要取t1和t2连接后的按t1.c2列升序的10个值，topn可以下压到连接算子之前，提前按t1.c2列升序后取10个值，再进行连接，可以减少t1表的数据量。

重写后的结果是正确的，由于topn的排序列仅包含t1表上的列，对于左外连接而言，t1表的结果都会保存，连接后的经过topn和直接对t1表取topn获得的t1表的行是一致的。

由于t1和t2连接时可能使用不同的连接算法导致顺序破坏和连接的产生结果集超过10行，所以保留重写后的SQL中外层查询的order和limit语句是也有必要的。





Tidb2.1的谓词下推
----

### 问题描述：
> 谓词：取值为 TRUE、FALSE 或 UNKNOWN 的表达式。 谓词用于 WHERE 子句和 HAVING 子句的搜索条件中，还用于 FROM子句的联接条件以及需要布尔值的其他构造中。 -- Microsoft SQL Server

> 连词：not、and和or

谓词下推是指将SQL中的用于过滤作用的谓词条件下推到更底层的位置执行，提前完成数据的过滤，减少后续算子处理的数据量，加快查询执行。

能够下推谓词条件主要包括having条件，where条件以及join on上的条件。


### 相关文件与结构体说明：

谓词下推的所有的相关代码都在`plan/rule_predicate_push_down.go`文件中 。

##### 数据结构与方法：
- `ppdSolver`:
	谓词下推解析器，只有一个optimize()方法，并无实质内容，仅调用传入的逻辑计划节点的`PredicatePushDown()`法。

- `addSelection()`:
	该函数的作用是将无法下推的谓词条件构造为LogicalSelection对象，插在当前logicalPlan节点的下推，其孩子节点是当前logiclaPlan节点的孩子。

- `concatOnAndWhereConds()`:
	该函数的作用是合并join on子句上的条件和where子句上的条件,where子句的条件作为参数传入。	

- `isNullRejected()`:
	该函数的作用是检查谓词条件是否满足空值拒绝，空值拒绝用于外连接消除。包含三种情况：1)如果它是内表(注：此处的内表指外连接，内连接时外表也满足)的谓词，在输入为NULL时返回UNKNOWN/FASLE，如`c1=10` ；2)如果它是包含null-rejected条件的连词作为合取,如`c1=10 and c2 is null`;3)如果它是null-rejected条件的析取,如`c1=10 or c2 =10`(注意：这里只能是null-rejected条件的析取，不能包含非null-rejected条件)。【附：个人认为可以补充的null-rejected情形还有一种是，where上的连接条件，如`where t1.c1=t2.c2`也是满足空值拒绝的，事实上，where上的连接条件作为等价于inner join的连接条件】

- `simplifyOuterJoin()`：
	该函数的作用是进行外连接消除，可有空值拒绝的谓词消除外连接，由于内连接可以下推更多的谓词，因此tidb会尽力消除外连接，具体消除过程见后面。

- `baseLogicalPlan.PredicatePushDown()`：
	LogicalPlan节点基类的谓词下推方法，子类的默认继承了该方法。该方法调用其子孩子的`PredicatePushDown()`方法进行自顶向下传递，无法下推的谓词将构造为LogicalSelection节点。

- `LogicalUnionAll`：
	遍历其孩子节点，将谓词下推到union算子的孩子节点下面。

- `LogicalProjection`：
	下推到project算子的孩子节点前，通过调用`expression.ColumnSubstitute()`函数替换待下压谓词的列名，由于project算子可能重命名过列名。

- `LogicalUnionScan`：
	tidb的代码注释提到该结构体只用于非只读事务中，其只有一个孩子节点，会尝试下推谓词到孩子节点之后将谓词（该谓词未知是否更改）追加到自己的条件中。

- `LogicalSelection`:
	其本身也代表着过滤的选择算子，会将本身的谓词条件和上层传递进来的谓词一起尝试下推到孩子节点。无法下推的谓词，调用`expression.PropagateConstant()`函数，对谓词的进行等价类推。

- `LogicalMaxOneRow、LogicalLimit`:
	对于这两个算子，禁止上层的谓词下推，	因为下推上层的谓词可能改变查询结果，但是会调用`baseLogicalPlan.PredicatePushDown(nil)` 递归调用孩子节点的谓词下推。

- `LogicalAggregation`:
	having子句中或外层查询被下推的谓词为常量或涉及到的列若是group by列可以下推到孩子节点，若无group by子句也可以下推，注意非group by列的谓词无法下推。 

- `DataSource`:
	该结构代表着基本表，它的谓词下推是把过滤条件加入到 CopTask 里面，最后会被通过 coprocessor 推给 TiKV 去做

- `LogicalJoin`：
	该结构体代表join算子，谓词下推到其孩子节点过程：首先，做外连接消除`simplifyOuterJoin()`,其次，从提取出下推的谓词，分成等值连接谓词`equalCond`, 左表的相关谓词`leftPushCond`,右表相关谓词` rightPushCond`,其他非等值连接谓词`otherCond`。然后根据join类型分别下压各个谓词。



	
### 实现：
重要的下推实现是将谓词下推到join的孩子节点以及外连接消除，其余的下推函数实现较简单。

- LogicalJoin中不同join类型可以下推的的谓词为：
	- `LeftOuterJoin, LeftOuterSemiJoin, AntiLeftOuterSemiJoin`:左孩子可下推的谓词是来自where和having以及外层查询下推的`leftPushCond`；右孩子可以下推的谓词是join on上右（内）表的相关谓词`p.RightConditions`。
	- `RightOuterJoin`:左孩子可下推的谓词是join on上右（内）表的相关谓词`leftPushCond`，右孩子可以下推的谓词是来自where和having以及外层查询下推的`rightPushCond`。
	- `SemiJoin, AntiSemiJoin`:由于此类型的半连接为内连接，所以，左右孩子可以下推的谓词是来自join on和where和having以及外层查询中与左右孩子相关谓词。
	- `InnerJoin`:左右孩子可以下推的谓词是来自join on和where和having以及外层查询中与左右孩子相关谓词。

  注：关于在join算子上的谓词下推，有个关键的处理函数 `expression.ExtractFiltersFromDNFs()` ,DNF代表析取or表达式，CNF代表合取and表达式。在该函数中会从or表示中提取过滤条件（但是我暂时未弄理解这个是如何提取出来的），然后加入需要下推的谓词中。`SemiJoin, AntiSemiJoin`下推的时候并用到该函数，是与inner join下推所不同的地方。


- `simplifyOuterJoin()`:
	外连接消除在tidb2.1中大致流程为，先确定内外表，然后先对孩子节点进行外连接消除，先内表，后外表，当内外表都已经完成外连接消除，则处理当前节点的外联连接消除，判断是否能进行外连接消除，是通过`isNullRejected()`函数检查内表的谓词是否是null-rejected。【注：这种顺序，其实可以调整为先处理内表外连接消除，然后是当前节点的外连接消除，根据当前外联接消除，生成join列的null-rejected条件用于递归消除外表的外连接】


	
### 举例说明：
最复杂的下推是join算子上的下推，所以下面给出一些具体的join算子上谓词下推例子：
##### (I) inner join:

- all position single table predicate can push down to base table level(position 1),
- other predicate can push down to join level or stay in aggregate level.

```sql
-- where:
select * from t1 inner join t2 on t1.c1=t2.c2 where t1.c1=10 ;
<=>
select * from (select * from t1 where t1.c1=10) a inner join (select * from t2 where t1.c2=10) b on a.c1=b.c2;

select * from t1 inner join t2 on t1.c1=t2.c2 where t1.c2=t2.c1;
<=>
select * from t1 inner join t2 on t1.c1=t2.c2 and t1.c2=t2.c1;

select * from t1 inner join t2 on t1.c1=t2.c2 where t1.c2=10 or t2.c1=10;
<=>
select * from t1 inner join t2 on t1.c1=t2.c2 and (t1.c2=10 or t2.c1=10);

-- join on:
select * from t1 inner join t2 on t1.c1=t2.c2 and t1.c2=10 and t2.c1=10;
<=>
select * from (select * from t1 where t1.c2=10) a inner join (select * from t2 where t1.c1=10) b on a.c1=b.c2;

-- having:
select t1.c2,t2.c1,sum(t1.c3) from t1 inner join t2 on  t1.c1=t2.c2 group by t1.c2,t2.c1 having t1.c2=10 and t2.c1=10 and sum(t1.c3)>0;
<=>
select t1.c2,t2.c1,sum(t1.c3) from  (select * from t1 where t1.c2=10) a inner join (select * from t2 where t1.c1=10) b on a.c1=b.c2 group by t1.c2,t2.c1 having sum(t1.c3)>0;

```

######  (II) left join:

- nullable side: the inner table of left jon
- nonullable side: the outer table of left join
- strict predicate: input NULL output NULL/false, eg. c2 is not null, c2<10
- not strict predicate: input NULL output other/true, eg. c2 is null,COALESCE(c2, 0)

```sql
-- where:
-- can push down strict predicate on where to nullable side table level
-- and push down strict and not strict predicate on where to nonullable side table level
-- it means:

select * from t1 left join t5 on t1.c1=t5.c2 where t5.c3 is not null;
<=>
select * from t1 inner join (select * from t5 where t5.c3 is not null)  b on t1.c1=b.c2 ;

--can push strict predicate to join on
select * from t1 left join t2 on t1.c1=t2.c2 where t1.c2=t2.c1;
<=>
select * from t1 inner join t2 on t1.c1=t2.c2 and t1.c2=t2.c1;


select * from t1 left join t5 on t1.c1=t5.c2 where t1.c3 is not null;
<=>
select * from (select * from t1 where t1.c3 is not null) a  left join t5 on a.c1=t5.c2 ;

select * from t1 left join t5 on t1.c1=t5.c2 where t1.c3 is null;
<=>
select * from (select * from t1 where t1.c3 is null) a  left join t5 on a.c1=t5.c2 ;


--can't push down no strict predicate to nullable side
select * from t1 left join t5 on t1.c1=t5.c2 where t5.c3 is null;
select t5.c2 from t1 left join t5 on t1.c1=t5.c2 where  COALESCE(t5.c2, 2) > 1;


-- join on:
-- can  push down strict and not strict predicate on join level to nullable side base table level 

select * from t1 left join t2 on t1.c1=t2.c2 and t2.c3 <3;
<=>
select * from t1 left join (select * from t2 where t2.c3 <3) b on t1.c1=b.c2;

select * from t1 left join t2 on t1.c1=t2.c2 and t2.c3 is null;
<=>
select * from t1 left join (select * from t2 where t2.c3 <3) b on t1.c1=b.c2;

--can't push down predicate to nonullable side 
select * from t1 left join t2 on t1.c1=t2.c2 and t1.c3 is null;
select * from t1 left join t2 on t1.c1=t2.c2 and t1.c3 <10;
select * from t1 left join t2 on t1.c1=t2.c2 left join t3 on t1.c1=t3.c2 and t2.c3 <10;


-- having:(same as where)
-- can push strict and not strict predicate on having to nonullable side table level
-- can push strict predicate on having to nullable side table level

select t1.c2,t1.c3,count(t2.c1) c from t1 left join t2 on t1.c1=t2.c2 group by t1.c2,t1.c3 having t1.c2 <10 and t1.c3 <10 and count(t2.c1) >=1;
<=>
select a.c2,a.c3,count(t2.c1) c from (select * from t1 where t1.c2 <10 and t1.c3 <10) a left join t2 on a.c1=t2.c2 group by a.c2,a.c3 having count(t2.c1) >=1;


select t1.c2,t1.c3,count(t2.c1) c from t1 left join t2 on t1.c1=t2.c2 group by t1.c2,t1.c3 having t1.c2 is null and count(t2.c1) >=1;
<=>
select a.c2,a.c3,count(t2.c1) c from (select * from t1 where t1.c2 is null) a left join t2 on a.c1=t2.c2 group by a.c2,a.c3 having count(t2.c1) >=1;


select t2.c2,t2.c3,count(t2.c1) c from t1 left join t2 on t1.c1=t2.c2 group by t2.c2,t2.c3 having t2.c2 <10 and t2.c3 <10 and count(t2.c1) >=1;
<=>
select b.c2,b.c3,count(b.c1) c from t1 inner join (select * from t2 where t2.c2 <10 and t2.c3 <10) b on t1.c1=b.c2 group by b.c2,b.c3 having count(t2.c1) >=1;

-- can't push down no strict predicate to nullable side
select t2.c2,t2.c3,count(t2.c1) c from t1 left join t2 on t1.c1=t2.c2 group by t2.c2,t2.c3 having t2.c3 is null and count(t2.c1) >=1;
```







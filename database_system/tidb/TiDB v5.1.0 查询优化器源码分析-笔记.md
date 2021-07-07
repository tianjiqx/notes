# TiDB v5.1.0 查询优化器源码分析-笔记

## 1. 配置

- 编辑器：vim。

- vim 配置：

  参考个人workspace项目的[.vimrc](https://github.com/tianjiqx/workspace/blob/master/.vimrc)文件。 快捷键使用参考[vim-go插件使用](https://github.com/tianjiqx/notes/blob/master/tools-tutorial/vim-go%E6%8F%92%E4%BB%B6%E4%BD%BF%E7%94%A8.md)

- TiDB源码版本tag v5.1.0 (2021.6.23)

  `commit 8acd5c88471cb7b4d4c4a8ed73b4d53d6833f13e`
  
- 编译问题

  - make失败，go包管理网址无法访问：proxy.golang.org，使用国内代理`go env -w GOPROXY=https:*//goproxy.cn*`



## 2.SQL执行流程

还是从SQL执行流程开始。由于时间太久，知道以前官方文档的源码分析是否过时，先网络搜一下别人的源码分析。根据知乎院长的TiDB学习笔记，可以看到，距离3年前分析TiDB2.1时，SQL连接处理入口还是没变，在server/server.go的onConn()开始。

- `func (s *Server) onConn(conn *clientConn)` server/server.go
  - `func (cc *clientConn) Run(ctx context.Context) `: 内部一个永循环体调用dispatch处理请求数据，server/conn.go
    - `func (cc *clientConn) dispatch(ctx context.Context, data []byte) error` 解析数据，请求类型，主要的查询请求ComQuery，server/conn.go
      - `func (cc *clientConn) handleQuery(ctx context.Context, sql string) (err error) `   处理查询，IUD语句，server/conn.go
        - `func (s *session) Parse(ctx context.Context, sql string) ([]ast.StmtNode, error) ` session/session.go，sql字符串解析为StmtNode，接口, 具体StmtNode定义在pingcap/parser/parser/ast/ast.go文件中
          - `ParseSQL(ctx context.Context, sql, charset, collation string) ([]ast.StmtNode, []error, error) ` session/session.go
        - `func (cc *clientConn) handleStmt(ctx context.Context, stmt ast.StmtNode, warns []stmtctx.SQLWarn, lastStmt bool) (bool, error) `  server/conn.go 处理执行语句
          - `func (tc *TiDBContext) ExecuteStmt(ctx context.Context, stmt ast.StmtNode) (ResultSet, error) ` server/driver_tidb.go
            - `func (s *session) ExecuteStmt(ctx context.Context, stmtNode ast.StmtNode) (sqlexec.RecordSet, error) ` session/session.go
              - `func (c *Compiler) Compile(ctx context.Context, stmtNode ast.StmtNode) (*ExecStmt, error) ` 转换抽象语法树ast为物理执行计划，executor/compiler.go
              - `func runStmt(ctx context.Context, se *session, s sqlexec.Statement) (rs sqlexec.RecordSet, err error) ` 执行物理计划，session/session.go
                - `func (a *ExecStmt) Exec(ctx context.Context) (_ sqlexec.RecordSet, err error) `  executor/adapter.go，  executor.ExecStmt 实现了接口sqlexec.Statement

注意：

session.Excute()方法已经被deprecated,取代的是session.ExecuteStmt()。最终还是走到Compiler.Compile() 方法。

- `func (c *Compiler) Compile(ctx context.Context, stmtNode ast.StmtNode) (*ExecStmt, error) ` 转换抽象语法树ast为物理执行计划，executor/compiler.go

  - `func Preprocess(ctx sessionctx.Context, node ast.Node, preprocessOpt ...PreprocessOpt) error ` planner/core/preprocess.go，预处理，解析表名，检查语句合法性

  - `func Optimize(ctx context.Context, sctx sessionctx.Context, node ast.Node, is infoschema.InfoSchema) (plannercore.Plan, types.NameSlice, error) ` planner/optimize.go，查询优化器入口

    - `func handleStmtHints(hints []*ast.TableOptimizerHint) (stmtHints stmtctx.StmtHints, warns []error) ` planner/optimize.go，hint解析

    - `func optimize(ctx context.Context, sctx sessionctx.Context, node ast.Node, is infoschema.InfoSchema) (plannercore.Plan, types.NameSlice, float64, error) ` planner/optimize.go，优化

      - `func (b *PlanBuilder) Build(ctx context.Context, node ast.Node)   (Plan, error) ` planner/core/planbuilder.go  ast node 转逻辑计划

        - `func (b *PlanBuilder) buildSelect(ctx context.Context, sel *ast.SelectStmt) (p LogicalPlan, err error) `  planner/core/logocal_pan_builder.go select  ast树转select 逻辑计划

      - CascadesPlanner enable：`func (opt *Optimizer) FindBestPlan(sctx sessionctx.Context, logical plannercore.LogicalPlan) (p plannercore.PhysicalPlan, cost float64, err error) `  planner/cascades/optimize.go  级联优化器入口

      - 否则，`func DoOptimize(ctx context.Context, sctx sessionctx.Context, flag uint64, logic LogicalPlan) (PhysicalPlan, float64, error) ` planner/core/optimizer.go ，做逻辑优化，物理优化

        - `func logicalOptimize(ctx context.Context, flag uint64, logic LogicalPlan) (LogicalPlan, error) ` planner/core/optimizer.go， 逻辑优化，应用优化规则，**注意join reorder在最终的逻辑计划生成时已经完成**

          > 	&gcSubstituter{},
          > 	&columnPruner{},
          > 	&buildKeySolver{},
          > 	&decorrelateSolver{},
          > 	&aggregationEliminator{},
          > 	&projectionEliminator{},
          > 	&maxMinEliminator{},
          > 	&ppdSolver{},
          > 	&outerJoinEliminator{},
          > 	&partitionProcessor{},
          > 	&aggregationPushDownSolver{},
          > 	&pushDownTopNOptimizer{},
          > 	&joinReOrderSolver{},  // join重排序(DP、贪心)
          > 	&columnPruner{},

        - `func physicalOptimize(logic LogicalPlan, planCounter *PlanCounterTp) (PhysicalPlan, float64, error) ` planner/core/optimizer.go，物理优化

          - `func (p *baseLogicalPlan) recursiveDeriveStats(colGroups [][]*expression.Column) (*property.StatsInfo, error) ` planner/core/stats.go，统计信息推导
            - `func (p *baseLogicalPlan) DeriveStats(childStats []*property.StatsInfo, selfSchema *expression.Schema, childSchema []*expression.Schema, _ [][]*expression.Column) (*property.StatsInfo, error) ` planner/core/stats.go，根据左右孩子的统计信息，推导父节点的统计信息
          - `func (p *baseLogicalPlan) findBestTask(prop *property.PhysicalProperty, planCounter *PlanCounterTp) (bestTask task, cntPlan int64, err error)`planner/core/find_best_task.go, 递归的方式处理孩子节点，将逻辑计划转换为物理计划，可能候选的物理计划存在多个，挑选最代价最小的物理计划。 
            - `func (p *baseLogicalPlan) getTask(prop *property.PhysicalProperty) task ` planner/core/plan.go 查询memo表，对于物理属性的task是否已经生成过
            - `func (p *LogicalJoin) exhaustPhysicalPlans(prop *property.PhysicalProperty) ([]PhysicalPlan, bool, error) ` planner/core/exhaust_physical_plans.go，逻辑join计划的穷举 （对于project 逻辑计划就一种物理实现），确定最佳连接算法。连接顺序的调整由逻辑计划生成。
              - `func (p *LogicalJoin) GetMergeJoin`
              - 
            - `func (p *baseLogicalPlan) enumeratePhysicalPlans4Task(physicalPlans []PhysicalPlan, prop *property.PhysicalProperty, addEnforcer bool, planCounter *PlanCounterTp) (task, int64, error) ` planner/core/find_best_task.go 物理计划转task
            - task保存有物理算子及其代价

        - `func postOptimize(sctx sessionctx.Context, plan PhysicalPlan) PhysicalPlan ` planner/core/optimizer.go，物理优化后的处理

          - `func enableParallelApply(sctx sessionctx.Context, plan PhysicalPlan) PhysicalPlan`  planner/core/optimizer.go，尝试并行化算子。

整体的优化框架和处理逻辑，还是和2.1 没有大的变化。 还可2.1的逻辑优化，物理优化的pdf总结。

join reorder：

- `func (s *joinReOrderSolver) optimize(ctx context.Context, p LogicalPlan) (LogicalPlan, error) ` planner/core/rule_join_reorder.go，重排join 顺序，代价的评判规则只考虑行数，最终得到一个代价最小的连接顺序。

  - `func (s *joinReOrderSolver) optimizeRecursive(ctx sessionctx.Context, p LogicalPlan) (LogicalPlan, error) ` planner/core/rule_join_reorder.go，分组join，递归，对每个组应用重排序算法

    - `func extractJoinGroup(p LogicalPlan) (group []LogicalPlan, eqEdges []*expression.ScalarFunction, otherConds []expression.Expression)`  planner/core/rule_join_reorder.go，提取join组

      >  "InnerJoin(InnerJoin(a, b), LeftJoin(c, d))" ,results in a join group {a, b, LeftJoin(c, d)}.

    - `func (s *joinReorderDPSolver) solve(joinGroup []LogicalPlan, eqConds []expression.Expression) (LogicalPlan, error)` planner/core/rule_join_reorder.go，DP方式重排序 （BFS），不做笛卡尔积的连接



>  TiDB实践System R 优化器框架的发现的缺点：
>
> 1.扩展性不好。每次添加优化规则都需要考虑新的规则和老的规则之间的关系，需要对优化器非常了解的同学才能准确判断出新的优化规则应该处在什么位置比较好。另外每个优化规则都需要完整的遍历整个逻辑执行计划，添加优化规则的心智负担和知识门槛非常高。(tidb 应用优化规则，需要完整遍历计划树，因此规则设计需要考虑所有的节点，嵌套子查询等复杂处理。)
>
> 2.搜索空间有限。部分逻辑优化的应用，需要考虑分布式执行的代价。任何决策，都可能错过最佳计划。需要人工干预。



## 3.Cascades 模型的优化器

**动机：**

- 传统多阶段优化（System R风格），逻辑优化的聚合下推、聚合上拉、子查询展开等并不是总是有益的
- 可扩展性差，即使都是有益的场景规则，很难添加新规则，需要仔细考虑优化规则的应用顺序，并且需要丰富的优化经验，发现各种优化规则
- 代价模型绑定，物理存储引擎的扩展，进行物理优化的扩展性差。



**Cascades 模型的观点：**

- 自顶向下的探索所有可能计算代价+memo 记录子表达式避免重复探索
- 逻辑计划经过模式匹配，应用逻辑转换规则，探索等价的逻辑表达式，逻辑表达式，再应用物理转换规则，生成物理表达式，变得可以计算代价，评估一个计划的代价。
- 代价最小的计划的计算是一个自底向上的过程。



TiDB cascades 优化器：

> 1. 首先将抽象语法树（AST）转换为初始的逻辑执行计划，也就是由 LogicalPlan 所表示的算子树。
> 2. Cascades Planner 将这棵初始的 LogicalPlan 树等价地拆分到 `Group` 和 `GroupExpr` (Expression 在代码中对应的具体数据结构) 中，这样我们便得到了 Cascades Planner 优化器的初始输入。
> 3. Cascades Planner 将搜索的过程分为了两个阶段，第一阶段是 Exploration ，该阶段不停地遍历整个 Group ，应用所有可行的 Transformation Rule，产生新的 Group 和 GroupExpr ，不停迭代直到没有新的 GroupExpr 诞生为止。
> 4. 在第二个阶段 Implementation 中，Cascades Planner 通过对 GroupExpr 应用对应的 Implementation Rule，为每一个 Group 搜索满足要求的最佳（Cost 最低）物理执行计划。
> 5. 第二阶段结束后，Cascades Planner 将生成一个最终的物理执行计划，优化过程到此结束，物理执行计划交给 TiDB 执行引擎模块继续处理。

代码实现处理流程：

- `func (opt *Optimizer) FindBestPlan(sctx sessionctx.Context, logical plannercore.LogicalPlan) (p plannercore.PhysicalPlan, cost float64, err error) `planner/cascades/optimize.go  级联优化器开始
  - `func (opt *Optimizer) onPhasePreprocessing(sctx sessionctx.Context, plan plannercore.LogicalPlan) (plannercore.LogicalPlan, error)` planner/cascades/optimize.go  预处理，完全有益的规则，列裁剪
  - `func Convert2Group(node plannercore.LogicalPlan) *Group`  planner/memo/group.go 逻辑计划初始化Root Group信息。
    - `func Convert2GroupExpr(node plannercore.LogicalPlan) *GroupExpr ` planner/memo/group.go 逻辑计划转组表达式。
      - `func Convert2Group(node plannercore.LogicalPlan) *Group`  planner/memo/group.go 递归调用，孩子节点生成group。
    - `func NewGroupWithSchema(e *GroupExpr, s *expression.Schema) *Group ` planner/memo/group.go，创建Group
  - `func (opt *Optimizer) onPhaseExploration(sctx sessionctx.Context, g *memo.Group) error ` planner/cascades/optimize.go，从root Group 开始探索等价的 组表达式
    - `func (opt *Optimizer) exploreGroup(g *memo.Group, round int, ruleBatch TransformationRuleBatch) error` planner/cascades/optimize.go，探索group。
      - `func (opt *Optimizer) exploreGroup(g *memo.Group, round int, ruleBatch TransformationRuleBatch) error` planner/cascades/optimize.go 对Group里的每个组表达式，先递归探索children的Group。
      - `func (opt *Optimizer) findMoreEquiv(g *memo.Group, elem *list.Element, round int, ruleBatch TransformationRuleBatch) (eraseCur bool, err error) `planner/cascades/optimize.go，应用TransformationRuleBatch的规则，探索组表达式的所有等价逻辑表达式，并插入到Group中。
  - `func (opt *Optimizer) onPhaseImplementation(sctx sessionctx.Context, g *memo.Group) (plannercore.PhysicalPlan, float64, error) ` planner/cascades/optimize.go，将Group的逻辑组表达式实现为物理组表达式。
    - `func (opt *Optimizer) implGroup(g *memo.Group, reqPhysProp *property.PhysicalProperty, costLimit float64) (memo.Implementation, error)` planner/cascades/optimize.go，将Group的逻辑组表达式实现为物理组表达式，并计算出代价最低的物理组表达式，并插入到group。
      - `func (opt *Optimizer) implGroupExpr(cur *memo.GroupExpr, reqPhysProp *property.PhysicalProperty) (impls []memo.Implementation, err error)`planner/cascades/optimize.go，逻辑组表达式实现为物理组表达式
        - 递归调用`implGroup` ，对孩子节点计算最低实现代价。
        - `CalcCost(outCount float64, children ...Implementation) `计算Implementation的代价
      - `func GetEnforcerRules(g *memo.Group, prop *property.PhysicalProperty) (enforcers []Enforcer) ` planner/cascades/enforcer_ruless.go , 生成属性强制规则（排序要求）
      - `func (e *OrderEnforcer) GetEnforceCost(g *memo.Group) float64 ` planner/cascades/enforcer_ruless.go 应用物理属性强制，计算需要满足排序属性的代价。
      - 调用`implGroup` 对本group，增加返回需要满足属性强制规则（顺序）的实现
      - `func (e *OrderEnforcer) OnEnforce(reqProp *property.PhysicalProperty, child memo.Implementation) (impl memo.Implementation) ` planner/cascades/enforcer_ruless.go，增加满足属性的具体物理算子
      - `func (g *Group) InsertImpl(prop *property.PhysicalProperty, impl Implementation) ` planner/memo/group.go ，插入满足物理属性的最低代价的实现。
  - `func (p *basePhysicalPlan) ResolveIndices() (err error)` planner/core/resolve_indices.go，解析索引信息? 没明白，似乎和执行有关，不是对物理计划本身再做调整。



[TiDB planner/cascades projects 开发计划](https://github.com/pingcap/tidb/projects/16) 最近更新还是在2021.02.09，还有15个TODO，看起来暂时推迟开发了。 并且根据[测试]() 发现 cascades的优化器并没有work，很令人奇怪。



TODO：orca，calcite 是如何实现cascades的细节（源码分析）

ORCA：

优化流程：

- Exploration
  - 探索Group内的所有等效的逻辑组表达式GroupExpression
  - opt处理孩子，完成孩子Exp的递归。
- Stats Derivation
  - 统计信息推导，在等效的GroupExpression中，选择误差传播最小的。
- Implementation
  - 逻辑组表达式GroupExpression生成物理执行计划
- Optimization
  - 属性强制，添加数据分布，排序要求，挑选代价最小的计划。
  - Optimization阶段完成属性强制(request)和cost计算，自顶向下从root group 开始应用属性。然后挑选满足opt.request的代价最小的物理组表达式
  - G0中物理组表达式的生成的对G1的opt.request,每个物理组表达式对孩子Group的req可能不同
  - 对一个group进行opt前需要exp和imp这个组，以及完成孩子group的opt



ORCA还用多线程并行加速优化的思想，改进优化时间。

或许可以考虑未来的优化器优化执行过程，是一个独立的线程池模块。多SQL语句总是有相近的连接和访问请求。

优化的过程可以使用缓存的最佳子计划来快速生成计划。

事实上，逻辑表达式的探索优化，实际在固定表，固定选择率（过滤条件），这样的情况，相同逻辑表达式最后生成的计划应该一致的。

对于计划缓存，虽然有类似的效果，但是实际去除参数后，如果在数据倾斜的情况下，缓存的计划可能并不是一个最优的计划。 而在大数据环境下，数据倾斜实际上是一个很常见的环境。





## 4.统计信息推导（Stats Derivation）

原始统计信息，是收集每张表的总行数，全局/分片(region)的各列的不同值个数，列的min，max值。高频值的选择率（单值查询，count min sketch, 源码对象NewCMSketch）(查看tidb源码StatsInfo只有Cardinality是单个map，只是topN）。GroupNDV是tidb对多列组合的不同值个数的统计（看起来是全局的）。

列直方图(Histogram,histogram.go)，具有列id，不同值个数，null值个数，分桶边界，桶（行数，不同值个数，重复次数）



统计信息推导，是指经过filter，join之后的统计信息估计。主要的内容是ndv值的推导。用ndv值估计连接结果大小。

- filter：列的敏感性，非求ndv列的选择率，独立分布均匀假设。（tidb也参考SQL server调整估计限制最多4次）

- join：
  - 基于region之间的笛卡尔积计算方式进行join，每两个region的连接可以视作表的连接，最后统计总的连接大小。
  - tidb：基于全局直方图信息的join，大小估计
    - region 边界对齐——假设均匀分布
    - min (NDV1,NDV2) （内连接）
    - 外连接处理



TiDB 统计信息支持全量、采样收集，时间列的增量收集。

（全量，统计信息更新代价？）



## REF

- [TiDB源码学习笔记：启动TiDB](https://zhuanlan.zhihu.com/p/304036138)
- [TiDB的后花园 - 知乎专栏](https://www.zhihu.com/column/newsql) 
- [SQL 性能调优](https://docs.pingcap.com/zh/tidb/stable/sql-tuning-overview) 
- [提案：基于 Volcano/Cascades 模型的 SQL Planner](https://github.com/pingcap/tidb/blob/master/docs/design/2018-08-29-new-planner.md)
- [提案：维护计划中的统计信息(直方图的统计信息推导)](https://github.com/pingcap/tidb/blob/master/docs/design/2018-09-04-histograms-in-plan.md)
- [提案：join 重排序设计](https://github.com/pingcap/tidb/blob/master/docs/design/2018-10-20-join-reorder-dp-v1.md) 推荐
- [TiDB 统计信息简介 ](https://docs.pingcap.com/zh/tidb/stable/statistics#%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF%E7%AE%80%E4%BB%8B)
- [TiDB in Action](https://book.tidb.io/)
- [Cascades Optimizer](https://zhuanlan.zhihu.com/p/73545345) 知乎[hellocode](https://www.zhihu.com/people/hellocode-ming) 的总结，推荐
- [揭秘 TiDB 新优化器：Cascades Planner 原理解析](https://zhuanlan.zhihu.com/p/94079481)
- [十分钟成为 Contributor 系列 | 为 Cascades Planner 添加优化规则](https://zhuanlan.zhihu.com/p/93811520)
- [CMU SCS 15-721 (Spring 2019) : Optimizer Implementation (Part II)](https://15721.courses.cs.cmu.edu/spring2019/slides/23-optimizer2.pdf) Andy Pavlo对优化器实现的总结，有关于cascades框架的执行过程演示，推荐










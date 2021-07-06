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

        - `func logicalOptimize(ctx context.Context, flag uint64, logic LogicalPlan) (LogicalPlan, error) ` planner/core/optimizer.go， 逻辑优化，应用优化规则，**注意join reorder在逻辑计划生成时已经完成**

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

    - `func (s *joinReorderDPSolver) solve(joinGroup []LogicalPlan, eqConds []expression.Expression) (LogicalPlan, error)` planner/core/rule_join_reorder.go，DP方式重排序 （BFS）



## 3.Cascades 模型的优化器

**动机：**

- 传统多阶段优化，逻辑优化的聚合下推、聚合上拉、子查询展开等并不是总是有益的
- 可扩展性差，即使都是有益的场景规则，很难添加新规则，需要仔细考虑优化规则的应用顺序，并且需要丰富的优化经验，发现各种优化规则
- 代价模型绑定，物理存储引擎的扩展，进行物理优化的扩展性差。



**Cascades 模型的观点：**

- 自顶向下的探索所有可能计算代价+memo 记录子表达式避免重复
- 



TiDB cascades 优化器：





[TiDB planner/cascades projects 开发计划](https://github.com/pingcap/tidb/projects/16) 最近更新还是在2021.02.09，还有15个TODO，看起来暂时推迟开发了。 并且根据[测试]() 发现 cascades的优化器并没有work，很令人奇怪。





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










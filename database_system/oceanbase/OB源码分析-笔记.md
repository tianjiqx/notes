# OB源码分析-笔记

## 1. 环境配置

- 编辑器：

  以前在学校时使用Qt creator 非常方便。但是不知为什么，现在用Qt 在索引ob源码时莫名崩溃。只能放弃。改用vim。（阿里的研发人员有的使用eclipse）

- vim 配置：

  参考个人workspace项目的[.vimrc](https://github.com/tianjiqx/workspace/blob/master/.vimrc)文件。 额外含有一点18年分析tidb的go配置。对于C++ 的插件最重要的是Ctags生成标签文件，实现自动补全、识别函数，变量，函数跳转。 更多使用快捷键，参考[Vim-cpp使用-笔记](https://github.com/tianjiqx/notes/blob/master/tools-tutorial/Vim-cpp%E4%BD%BF%E7%94%A8-%E7%AC%94%E8%AE%B0.md)

- OB源码版本2021.6.30 （根据ob_cluster_version.h `#define CLUSTER_CURRENT_VERSION CLUSTER_VERSION_3100` 可知当前应是3.1.0版本，根据tpc-c,tpc-h榜单上显示的版本2.2和3.2，确实基本是最新的代码了，而且应该是相对稳定的版本）

  `commit 99866eb99df8ec3d65ebdfabaee61ef551f0cc90`
  
- 开始：

  ```shell
  # 克隆
  https://github.com/oceanbase/oceanbase.git
  cd oceanbase/
  # ctags 生成标签, -R 递归生成，忽略警告
  ctags -R
  # 打开文件obmp_query.cpp，开始源码分析
  vi src/observer/mysql/obmp_query.cpp
  ```

  (TODO:GDB 调试配置)

## 2. SQL执行流程

OB的整体架构可以直接看官网的文档很详细，作为数据库，了解系统，最基础应该还是从了解SQL的执行过程，来初步认识系统。

找到查询的处理类`ObMPQuery`，通过linux的ag工具grep到在这个文件`src/observer/mysql/obmp_query.cpp`

- **入口函数**：`int ObMPQuery::process()`

  - 切分多语句sql，`parser.split_multiple_stmt(sql_, queries, parse_stat))`
  - 批量优化`ObMPQuery::try_batched_multi_stmt_optimization`
    - 尝试合并多条update语句成一条
    - `ObMPQuery::process_single_stmt` 同时处理多条语句，接收`ObMultiStmtItem`对象参数，内包含queries信息，query的索引号，是否作为多条语句的一部分处理
  - 批量优化未开启或只有一条语句，未做优化，迭代queries，执行`ObMPQuery::process_single_stmt`处理单条语句

- **单语句处理**：`int ObMPQuery::process_single_stmt(const ObMultiStmtItem& multi_stmt_item, ObSQLSessionInfo& session,
      bool has_more_result, bool force_sync_resp, bool& async_resp_used, bool& need_disconnect)`
  - 初始化参数，检查更新schema，时区信息，清理状态，重试略过
  - 核心`ObMPQuery::do_process`方法
    - sql长度检查，最长64K
    - 持有关键对象的指针` ObMySQLResultSet*,ObPhysicalPlan*,ObQueryExecCtx*` 用于执行前初始化，执行后处理（设置影响行数，报错信息等等）
      - ObResultSet包含物理执行计划和一些元信息
    - 进入ObSql处理逻辑，生成物理计划，保存在result中`gctx_.sql_engine_->stmt_query(sql, ctx_, *result)))`
    - 返回结果` int ObMPQuery::response_result(ObQueryExecCtx& query_ctx, bool force_sync_resp, bool& async_resp_used)` 通过query_ctx获取result，执行物理计划，迭代输出结果。
      - 实际由ObAsyncPlanDriver和ObSyncPlanDriver `response_result()`完成 
        - `open(),response_query_result(), close()`
          - 获取数据，调用`inline int ObMySQLResultSet::next_row(const ObNewRow*& obmr)`

ObSql类(`src/sql/ob_sql.cpp`)，将sql语句从字符串转换为物理执行计划。

- **入口函数**：`int ObSql::stmt_query(const common::ObString& stmt, ObSqlCtx& context, ObResultSet& result)`

  - 直接进`handle_text_query(stmt, context, result))`
    - 会先尝试从物理计划缓存中，获取计划
    - 机票去不到，进入`int ObSql::handle_physical_plan(
          const ObString& trimed_stmt, ObSqlCtx& context, ObResultSet& result, ObPlanCacheCtx& pc_ctx, const int get_plan_err)` 方法生成物理计划

-  `handle_physical_plan` 进行语法解析，逻辑、物理计划生成

  - `ObSql::handle_parser` 语法解析

  - `ObSql::generate_physical_plan` 逻辑计划，物理计划生成

    - `ObSql::generate_stmt` 语法解析结果ObStmt生成
    - `ObPrivilegeCheck::check_privilege_new` 权限检查
    - `ObSql::transform_stmt` ObStmt做一些转换处理（重写，类似逻辑优化）（既然来源于变形金刚，或许应该叫变形而不是转换？:D）
      - ObTransformerImpl(`sql/rewrite/ob_transformer_impl.cpp`)的有子类ObTransformOuterJoinLimitPushDown等
        - `ObTransformerImpl::do_transform` 应用转换规则，默认迭代10次
      - ObTransformerImpl收集所有ObTransformRule的实现
      - 在`src/sql/rewrite/ob_transform_xxx` 大量重写的规则
    - **`ObSql::optimize_stmt`** 使用查询优化优化器ObOptimizer(`sql/optimizer/ob_optimizer.cpp`) 执行优化，并生成逻辑执行计划
      - `optimizer.optimize(stmt, logical_plan)))` 调用优化器执行优化和逻辑计划生成
    - `ObSql::code_generate` 生成物理计划
      - `ObCodeGenerator::generate`  生成旧引擎执行计划/新引擎执行计划(可参考导读是10)
        - `ObCodeGenerator::generate_old_plan` 
        - `ObCodeGenerator::generate_operators`
          - `ObStaticEngineCG::generate` ObStaticEngineCG 继承 ObCodeGeneratorImpl
            - `ObStaticEngineCG::postorder_generate_op` 后序遍历生成
              - `ObOperatorFactory::generate_spec`创建算子
              - `ObStaticEngineCG::generate_spec_basic` 根据具体逻辑算子，填充信息
              - `ObStaticEngineCG::generate_spec_final` 个别算子共同额外共同处理逻辑

  - `ObSql::pc_add_plan` 物理计划添加到缓存

    

- `ObOptimizer::optimize` 查询优化
  - `plan = ctx_.get_log_plan_factory().create(ctx_, stmt)))` 调用`ObLogPlanFactory::create` 创建逻辑计划对象(ObSelectLogPlan,ObInsertLogPlan,ObDeleteLogPlan等)
  - 调用逻辑计划(如ObSelectLogPlan)的`generate_plan()` 填充完整的逻辑计划信息，并在这个过程中执行查询优化
- `ObSelectLogPlan::generate_plan()` select语句的逻辑计划生成
  
  - `ObSelectLogPlan::generate_raw_plan()` 生成原始的逻辑执行计划
    - `ObSelectLogPlan::ggenerate_plan_for_set` 带有集合算子的语句生成
    - `ObSelectLogPlan::ggenerate_plan_for_plain_select` 普通select语句生成
      - 调用基类的方法`ObLogPlan::generate_plan_tree()` 生成基本表访问路径，执行计划，join的顺序
        - `ObLogPlan::generate_join_orders()` 生成连接信息
          - `ObLogPlan::get_table_items` 获取所有的表信息（包含join生成的表）
          - `ObLogPlan::get_base_table_items` 生成基本表信息
          - `ObLogPlan::generate_base_level_join_order` 生成基本连接顺序，`ObJoinOrder*`的数组，大小对应基本表的个数（todo:没对应join算子的个数）
          - `ObLogPlan::pre_process_quals`处理 join on，where条件
          - 对每个`ObJoinOrder`调用`ObJoinOrder::generate_base_paths()` 生成基本访问路径 
            - 基本表`ObJoinOrder::generate_normal_access_path()`
              - `ObJoinOrder::generate_access_paths(PathHelper& helper)`
                - `ObOptEstCost::estimate_width_for_table` 行数，宽度估计（ob say：bad design）
                - `ObJoinOrder::add_table`
                  - `add_table_by_heuristics`,`prunning_index`
                  - `ObJoinOrder::create_access_path` 单表的访问路径`AccessPath`对象生成
                    - 选择率，采样信息
                    - 是否全局索引，索引回表行数，代价估计的信息等等
                - `ObJoinOrder::estimate_size_and_width_for_access` 估计表的行数，宽度
                  - `ObJoinOrder::estimate_rowcount_for_access_path`
                    - `ObOptEstCost::estimate_row_count` 行数，访问的分区数量等
                - `ObJoinOrder::compute_cost_and_prune_access_path` 计算各访问路径代价并剪枝
                  - ` AccessPath::estimate_cost()`
          - `ObLogPlan::init_leading_info` hint信息处理
          - `ObLogPlan::init_bushy_tree_info` 初始化bushy tree连接的信息
          - `ObLogPlan::generate_join_levels_with_DP` 动态规划调整连接顺序，低于10张表
            - ` ObLogPlan::generate_single_join_level_with_DP` 一趟DP
              - `ObLogPlan::inner_generate_join_order` 连接两个join order
                - `ObJoinOrder::generate_join_paths` 生成连接路径
                  - `ObJoinOrder::inner_generate_join_paths`
                    - `ObJoinOrder::generate_mj_paths` merge join
                    - `ObJoinOrder::generate_hash_paths` hash join
                    - `ObJoinOrder::generate_nl_paths` nest loop join
                      - `ObJoinOrder::choose_best_inner_path` 基于代价挑选孩子节点的最佳路径(只左子树？)
                      - `ObJoinOrder::find_minimal_cost_path`（右子树？）最终的最低代价路径，1个
                      - `ObJoinOrder::create_and_add_nl_path` 创建NL路径，连接左右子树（多个，子树路径可能有多个interesting path）
            - ZigZag tree，bushy tree 通过枚举生成
          - 否则`ObLogPlan::generate_join_levels_with_linear`
      - `ObLogPlan::candi_init()` 候选计划初始化
        - `ObLogPlan::create_plan_tree_from_path` 根据interesting paths生成多个逻辑候选计划
        - 更新候选计划代价
    - `ObLogPlan::get_current_best_plan(ObLogicalOperator*& best_plan)` 从候选计划中挑最佳计划
  - ` ObLogicalOperator::adjust_parent_child_relationship()` 调整计划，未理解目的
  - `ObLogPlan::plan_traverse_loop`  模板方法，根据参数遍历原始执行计划，执行任务，例如ALLOC_EXCH根据算子的分区信息，插入ObLogExchange。
    - `ObLogPlan::plan_tree_traverse`  
      - `ObLogicalOperator::do_plan_tree_traverse` 根据参数会走到的实际工作方法
        - `ObLogicalOperator::do_post_traverse_operation` 包含分配exchanged算子的处理
  - ` ObLogPlan::calc_plan_resource` 检查资源，分析DFO, 设置worker数量
    - `ObPxResourceAnalyzer::analyze` 资源分析的工作类（px是并行执行的缩写？）
      - `ObPxResourceAnalyzer::convert_log_plan_to_nested_px_tree` 
        - `ObPxResourceAnalyzer::create_dfo_tree`根据ObLogExchange算子，生成在垂直方向上划分数据流对象DFO



TODO： 添加日志，构建后ODB部署运行，使用2表，3表。观察DP 计划生成过程。

并行执行的优化

```
//src/sql/optimizer/ob_select_log_plan.cpp
plan_traverse_loop(ALLOC_LINK,
                 ALLOC_EXCH,
                 ALLOC_GI,
                 ADJUST_SORT_OPERATOR,
                 PX_PIPE_BLOCKING,
                 PX_RESCAN,
                 RE_CALC_OP_COST,
                 ALLOC_MONITORING_DUMP,
                 OPERATOR_NUMBERING,
                 EXCHANGE_NUMBERING,
                 ALLOC_EXPR,
                 PROJECT_PRUNING,
                 ALLOC_DUMMY_OUTPUT,
                 CG_PREPARE,
                 GEN_SIGNATURE,
                 GEN_LOCATION_CONSTRAINT,
                 PX_ESTIMATE_SIZE,
                 GEN_LINK_STMT))
```



- 在OB 的tech talk 中谈到二阶段分布式计划优化，在第二阶段的并行优化，是使用启发式规则选择算子的分布式算法，是可能错过最优执行计划的，而在memsql 优化器的论文中也提到group by是否下推这样的原来可以只根据行数计算，在分布式执行环境下，最终真实的代价发生了改变。
- 二阶段分布式计划，优点是简单，搜索空间小。
- OB对于二阶段分布式计划优化的再优化思路，在第一阶段，考虑算子的分布式实现，维护物理属性，保留一些代价最小，有interesting order，intersting分区信息的计划，来缓解最优计划错过的可能。（这一点的思路，可能参考了pg传统优化器，保留次优计划的思想）
- 可以看出OB优化器的实现思路，还是在传统优化器基础上，考虑分布式执行环境而增加优化器计划的处理。多阶段优化的思路，很现实，能work，优化器优化时间性能可以保证。
  - 但是从系统的角度，不如cascade框架的优化器（如orca）现代。个人品味现在也更欣赏orca，memsql 优化器这样根据分布式系统环境重新设计的查询优化器来的优雅，扩展性更好，符合分布式系统设计的味道（高可用，可扩展，高性能）（OB1.0后将原来四角色合并成单角色的ObServer，具有所有角色的能力，是巨大的重构，这勇气和努力值得赞赏）。
  - 从工程角度，查询优化器本身与系统绑定（历史遗留，设计问题），细节藏着魔鬼（如原表经过不同列条件的选择率过滤后，NDV值估计，以及多次估计后的结果），能够根据系统的执行框架，完成各种优化功能，就已经实属不易。并且传统的和现代的优化器，优化时间，优化效果究竟如何，只有实际检验业务才能知道，可能是各有优劣场景。OB优化器的实现逻辑清晰，考虑到边角内容很多，代码质量很高，是值得学习的。

## 3. 统计信息

统计信息主要代码路径在：src/share/stat。看起来有2个版本，ob_opt_column_stat.h ，对列的统计信息增加了直方图。统计信息有partitionid，应该还是按分区收集，并非全局的。（OB不是整表的是为了统计全表的完整统计信息，需要sort，收集和维护更新代价太大，在交行做的cbase也是如此，并且还没有直方图）

表的统计信息，带有sstable ，memetable 行数信息，宏，微块的数量信息

todo：统计信息的推导，应当是按分区，一一连接。





## REF

- [开源数据库OceanBase代码导读(1)](https://zhuanlan.zhihu.com/p/379437192) 真"导"读，给入口，并非源码分析
- [开源数据库OceanBase- 知乎专栏](https://www.zhihu.com/column/c_1386628099518402560) 专栏包含代码导读内容
- [开源OB官网-文档](https://open.oceanbase.com/docs) 架构、模块设计
- [OceanBase TechTalk #4 杭州站 查询优化主题](https://tech.antfin.com/community/activities/553/review) 查询优化器实践、并行执行引擎，其他talk有事务等相关主题
- [OceanBase源码阅读工具-Eclipse篇](https://zhuanlan.zhihu.com/p/380610508)

- [TPC-C性能测试排行](http://tpc.org/tpcc/results/tpcc_results5.asp)
- [TPC-H 性能测试排行](http://tpc.org/tpch/results/tpch_perf_results5.asp?resulttype=all)
- [TPC-DS V3性能测试排行](http://www.tpc.org/tpcds/results/tpcds_perf_results5.asp?resulttype=all)

- [杨传辉：从一体化架构，到一体化产品，为关键业务负载打造一体化数据库](https://open.oceanbase.com/blog/7747032352)
  - 基线数据共享存储，总的接近一份数据的存储成本 
- [基于OceanStor Dorado的OceanBase数据库存算分离最佳实践.pdf](https://www.modb.pro/doc/128811)
- [OceanBase、腾讯云、华为云联合发布《数据库存算分离最佳实践》！](https://www.modb.pro/db/1782671167769833472)
  - 创建 LUN 并映射给主机方式使用远端存储，数据库不感知存储
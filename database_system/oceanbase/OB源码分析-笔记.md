# OB源码分析-笔记

## 1. 环境配置

- 编辑器：

  以前在学校时使用Qt creator 非常方便。但是不知为什么，现在用Qt 在索引ob源码时莫名崩溃。只能放弃。改用vim。

- vim 配置：

  参考个人workspace项目的[.vimrc](https://github.com/tianjiqx/workspace/blob/master/.vimrc)文件。 额外含有一点19年分析tidb的go配置。对于C++ 的插件最重要的是Ctags生成标签文件，实现自动补全、识别函数，变量，函数跳转。 更多使用快捷键，参考[Vim-cpp使用-笔记](https://github.com/tianjiqx/notes/blob/master/tools-tutorial/Vim-cpp%E4%BD%BF%E7%94%A8-%E7%AC%94%E8%AE%B0.md)

- OB源码版本2021.6.30 （根据ob_cluster_version.h `#define CLUSTER_CURRENT_VERSION CLUSTER_VERSION_3100` 可知当前应是3.1.0版本）

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

作为数据库，了解系统，最基础应该还是从了解SQL的执行过程，来初步认识系统。

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
  - `ObSql::pc_add_plan` 物理计划添加到缓存

- `ObSql::generate_physical_plan`

  

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
                      - `ObJoinOrder::create_and_add_nl_path` 创建NL路径，连接左右子树（多个，子子树路径可能有多个interesting path）
            - ZigZag tree，bushy tree 通过枚举生成
          - 否则`ObLogPlan::generate_join_levels_with_linear`
      - `ObLogPlan::candi_init()` 候选计划初始化
        - `ObLogPlan::create_plan_tree_from_path` 根据interesting paths生成多个逻辑候选计划
        - 更新候选计划代价
    - `ObLogPlan::get_current_best_plan(ObLogicalOperator*& best_plan)` 从候选计划中挑最佳计划



## REF

- [开源数据库OceanBase代码导读](https://zhuanlan.zhihu.com/p/379437192)
- [开源数据库OceanBase](https://www.zhihu.com/column/c_1386628099518402560)
- [开源OB官网-文档](https://open.oceanbase.com/docs)
- [OceanBase TechTalk #4 杭州站 查询优化主题](https://tech.antfin.com/community/activities/553/review)


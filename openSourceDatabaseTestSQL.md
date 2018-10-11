##开源数据库的回归测试SQL案例说明


该文档旨在介绍一系列的开源数据库自带的回归测试SQL案例集的文件目录说明，用于新开发数据库或者其他现有数据库能够重复吸收数据库开源社区的已有的测试案例集，保证数据库的查询正确性。

###ORCA

ORCA是Pivotal公司开源的一个独立的查询优化器特色是可以衔接到不同的大数据处理平台上，优化框架采用了先进、可扩展的Volcano / Cascades 框架。github地址:https://github.com/greenplum-db/gporca (分析版本979545ae37084f4bc9f11489b2722a3e8bfd9978)

ORCA文件目录说明：
- cmake:编译设置
- concurse:
- data:
  - dxl: 定义的dxl输入 ，测试案例
- libgpdbcost: orca的代价模型、代价公式，filter代价，scan代价 ，sort代价，NLJoin代价等等
- libgpopt:核心模块，定义了查询优化器核心组件，如其论文中的优化阶段的，search，translate，optimizer
- libgpos: 操作系统接口
- libnaucrates: 统计推导？
- scripts:**包含回归测试案例集 scripts/log\_runner/sql/**，包含2w多条测试sql，详细说明见readme
- server: 服务进程入口，单元测试


###postgreSQL




###MySQL







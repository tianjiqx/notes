## 开源数据库的回归测试SQL案例说明


该文档旨在介绍一系列的开源数据库自带的回归测试SQL案例集的文件目录说明，用于新开发数据库或者其他现有数据库能够重复吸收数据库开源社区的已有的测试案例集，保证数据库的查询正确性。

### ORCA

ORCA是Pivotal公司开源的一个独立的查询优化器特色是可以衔接到不同的大数据处理平台上，优化框架采用了先进、可扩展的Volcano / Cascades 框架。github地址:https://github.com/greenplum-db/gporca (分析版本979545ae37084f4bc9f11489b2722a3e8bfd9978)

ORCA文件目录说明：
- cmake:编译设置
- concurse:
- data:
 - dxl: 定义的dxl输入 ，测试案例
 - test:少量测试sql，与期望
- libgpdbcost: orca的代价模型、代价公式，filter代价，scan代价 ，sort代价，NLJoin代价等等
- libgpopt:核心模块，定义了查询优化器核心组件，如其论文中的优化阶段的，search，translate，optimizer
- libgpos: 操作系统接口
- libnaucrates: 统计推导？
- scripts:**包含回归测试案例集 scripts/log\_runner/sql/**，包含2w多条测试sql，详细说明见readme
- server: 服务进程入口，单元测试


### PostgreSQL

PostgreSQL是一个开源的功能丰富，性能强大的单机关系型数据库，号称世界上功能最强大的数据库，包括支持图数据库引擎，josn等复杂数据类型，目前在db-engining 排名第四。地址：https://www.postgresql.org/ (分析版本10.1)

PostgreSQL文件目录说明：
- config: 相关数据库配置文件
- contrib:开源社区贡献功能目录
- doc:pg用户文档
- src:主要源代码与测试sql
 - test:测试目录
  - regess:**回归测试**
   - data: 测试数据
   - sql: 测试SQL案例集，按子句功能划分，如join，limit等等
   - expected:sql执行期望结果
	 - input:数据导入，更新等命令
	 - output:input语句执行结果
	- isolation: 隔离级别测试
	- examples: 少量sql测试案例
 - backend:数据库后台进程代码
 - common:通用代码

### MySQL







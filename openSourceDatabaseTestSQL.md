## 开源数据库的回归测试SQL用例说明


该文档旨在介绍一系列的开源数据库自带的回归测试SQL用例集的文件目录说明，用于新开发数据库或者其他现有数据库能够重复吸收数据库开源社区的已有的测试用例集，保证数据库的查询正确性。

### ORCA

ORCA是Pivotal公司开源的一个独立的查询优化器特色是可以衔接到不同的大数据处理平台上，优化框架采用了先进、可扩展的Volcano / Cascades 框架。github地址:https://github.com/greenplum-db/gporca (分析版本979545ae37084f4bc9f11489b2722a3e8bfd9978)

ORCA文件目录说明：
- cmake:编译设置
- concurse:
- data:
 - dxl: 定义的dxl输入 ，测试用例
 - test:少量测试sql，与期望
- libgpdbcost: orca的代价模型、代价公式，filter代价，scan代价 ，sort代价，NLJoin代价等等
- libgpopt:核心模块，定义了查询优化器核心组件，如其论文中的优化阶段的，search，translate，optimizer
- libgpos: 操作系统接口
- libnaucrates: 统计推导？
- scripts:包含**回归测试用例集 scripts/log\_runner/sql/installcheck-workload.sql**，包含2w多条测试sql,测试输出在scripts/log\_runner/logs/installcheck-run.csv，详细说明见readme
- server: 服务进程入口，单元测试


### PostgreSQL

PostgreSQL是一个开源的功能丰富，性能强大的单机关系型数据库，号称世界上功能最强大的数据库，包括支持图数据库引擎，json等复杂数据类型，目前在db-engining 排名第四。地址：https://www.postgresql.org/ (分析版本10.1)

PostgreSQL文件目录说明：
- config: 相关数据库配置文件
- contrib:开源社区贡献功能目录
- doc:pg用户文档
- src:主要源代码与测试目录
  - test:测试目录
    - regess:**回归测试**
      - data: 测试数据
      - sql: `.sql`文件为测试用例，按子句功能划分，如join，limit等等
      - expected:sql执行期望结果
      - input:数据导入，更新等命令
      - output:input语句执行结果
	 - isolation: 隔离级别测试
	 - examples: 少量sql测试用例
 - backend:数据库后台进程代码
 - common:通用代码

### MySQL


MySQL是最流行的开源关系型数据库，目前仍在大量被中小企业使用，鉴于用户众多，后来的新NewSql都宣称兼容mysql的语法。地址：https://www.mysql.com/ (分析版本8.0.12)

MySQL测试文件目录说明:
- mysql-test:mysql**回归测试目录**,具体可参考官方说明:https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_MYSQL_TEST_RUN.html
  - t: `.test`后缀的测试用例,主要是SQL查询正确性的案例，包括bug问题的测试用例
  - r: `.result`后缀的为测试用例结果，对应t目录的用例
  - suite:一些其他的按功能分目录的测试案例
    - stress: 压力测试，测试集同样按t,r目录组织  
    - json: json类型的测试案例
  - std_data:测试数据



### SQLite

SQLite是一个高可用的，零配置，嵌入式的微型开源数据库系统库,由于体量小,被广泛的部署在各种设备中如安卓。地址:https://www.sqlite.org/index.html (分析版本3.23)

SQLite文件目录说明:
- art: 图标
- autoconf: 自动配置
- ext: 扩展
- mptest: 并发测试
- src: 源码目录
- tool: 工具
- vsixtest: 界面测试？
- test: **回归测试用例**,包含1000+`.test`后缀的测试用例,注意内中包括一些SQLite定义的一些语法，重用前，需要相关脚本处理后，提取其中的测试sql
  

### OceanBase

Oceanbase0.4.2是阿里巴巴2014年开源出来的分布式数据库，之后没有继续开源，但是在内部已经迭代到2.0,号称金融级的分布式数据库系统。地址:https://github.com/alibaba/oceanbase (分析版本0.4.2)

OceanBase文件目录说明:
- doc: OB相关安装文档，设计文档，用户使用文档
- src: 源代码
- test: 单元测试
- tool: 数据库工具以及测试用例
  - deploy: **回归测试用例**
    - mysql_test: 测试用例
      - t: `.test`文件是测试用例
      - r: `.result`文件是对应的测试结果
  - obtest: OB的功能模块测试用例

### TiDB

TiDB是pingCAP开发的一款支持HTAP负载的分布式数据库，底层存储引擎为KV系统的TiKV，分析型任务可以使用TiSpark，目前仍在快速迭代中，在github上有着活跃活动。地址:https://github.com/pingcap/tidb (分析版本v2.1.0-rc.3-25-g3104c87)

TiDB文件目录说明:
- 详细目录的介绍见TiDB官方介绍:https://github.com/ngaut/builddatabase/blob/master/tidb/sourcecode.md
- 测试用例:TiDB由于使用GO语言开发，其测试案例都依附在`xxx_test.go`文件中，例如`tidb/excutor/join_test.go`,并未采取mysql方式集中式的组织在一起，好处是对于xtidb自身的开发者而言方便了解定位某个模块的测试用例，避免bug，坏处是不够集中，无法利用到其他数据库，而且使用`tk.MustQuery()`和`result.Check(testkit.Rows("<nil> <nil> 1 1"))`进行执行SQL测试和结果验证。



### 总结

在上面我们列举了很多的开源数据库，但是从测试用例重用方便性上看，最方便的还是重用mysql的测试案例，一方面作为现在数据库SQL语法的事实标准，另一方面通过`.test`和`.result`可以方便直接在其他的数据库系统上重用测试用例和结果集，而其他数据库的测试用例的输入输出带有一定自定义的语法或格式，需要一定处理。建议以mysql的测试用例为主，其他数据库的选择性的挑选一些测试用例按mysql格式，丰富测试用例。

github上也能发现一些测试用例，巨杉数据库？测试用例(https://github.com/chanplion/new_testcases) ，不过目前我暂未发现一个特别好的已经总结好的方便使用的测试用例集。

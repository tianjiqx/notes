# TensorBase-笔记

## 1. 背景

TensorBase用开源的文化和方式，重新构建一个Rust编写的实时数据仓库，用于海量数据的存储和分析。



优点：

- All in Rust
  - 借助rust语言的高性能(c/c++)，无GC，内存、线程安全性。
- ClickHouse协议兼容
  - 用Rust实现了一个高性能的ClickHouse SQL方言解析器和TCP通讯协议栈
  - ClickHouse TCP客户端可以无缝连接TensorBase
- 基于Apache arrow-rs，DataFousion获取高性能分析能力。
  - 柱状的内存数据格式
  - 数据交换Copy-free，Rust语言机制带来的Lock-free，Async-free，Dyn-free
  - 项目外依赖减少（放到本地），以减少开发者重新编译时间



缺点：

- 还是起步的demo原型概念验证的阶段
  - 目前只是对于单表的聚合操作，相比clickhouse有明显的优势3X（并且数据完全加载进内存了，如果涉及磁盘读取，CH由于数据压缩，反而具有更好的性能）。
  - 之前在时间相关的函数处理上，会弱与CH，另外涉及列存个数的数据的shuffle，带有Join的SQL的性能是值得怀疑的。
    - TODO（CH，DataFusion的join原理）





## 2. 基本架构

![](tensorbase笔记图片/base_arch.jpg)

- Base Server
  - 服务接口层，连接协议层，提供数据的写入和查询入口。（与clickhouse的Server层作用一致）
  - 基于改造的Actix事件循环，取代tokio默认async表达层的实现
- Meta/Runtime/Storage
  - 元数据层、运行时层和存储层
  - 存储层使用Partition Tree的数据结构，数据直接写入分区文件，不compaction
- Engine
  - 执行引擎层，使用改造过的Apache Arrow和DataFusion，免数据SerDe。
  - more [Apache Arrow 笔记](https://github.com/tianjiqx/notes/blob/master/big_data_system/Apache%20Arrow.md)
- 其他组件
  - base
    - 通用工具库
  - lang
    - 语言层，ClickHouse兼容解析和表示层
  - lightjit
    - 类表达式JIT引擎



[计划 issue114](https://github.com/tensorbase/tensorbase/issues/141)  和 [2021 夏季开源推广计划](https://github.com/tianjiqx/tensorbase/blob/main/docs/summer_2021_ospp.md)：

- 分布式集群。 

  - 基于DataFusion的Ballista，类ClickHouse的简易（半人工）分布式集群方案。已经完成。

- 存储层增强

  - 引入主键

- 查询引擎

  - Arrow和Data Fusion查询内核性能改进
  - TPC-H其他性能

- Server

  - MySQL协议支持
  - Clickhouse http协议增强

  

## 3. 使用

```shell
# debug 版本，(fast compilation but slow run),
# cargo run --bin server -- -c crates/server/tests/confs/base.conf
cargo run --bin server -- -c qxbase.conf

# release 版本
cargo run --release --bin server -- -c crates/server/tests/confs/base.conf


# 连接
clickhouse-client --port 9528

```

测试sql：

```
create table employees (id UInt64, salary UInt64) ENGINE = BaseStorage
insert into employees values (0, 1000), (1, 1500)
select count(id) from employees
select avg(salary) from employees


show tables
```





## 4.  源码分析

环境配置：

IDEA2021.1 + rust 插件 



代码版本：

commit id ：`c39cc0adc2ce46474f6addbc7f4bf2e16788df7d`



- 1） RUN/DEBUG配置:

run --bin server -- -c qxbase.conf

> qxbase.conf 是拷贝server/tests/confs/base.conf，修改内meta_dirs，data_dirs配置

![](tensorbase笔记图片/Snipaste_2021-07-15_02-24-25.png)



建议现在本地 cargo build完成编译，避免idea 执行build，导致内存不足而卡死。

注意，社区版不支持debug方式运行！



- 2) 使用 [GDBUI](https://github.com/cs01/gdbgui)  进行调试 

使用Attach to Process模式，Ubuntu 20.04，直接下载二进制的gdbui包。

```shell
# 1. 运行TensorBase (debug)
cargo run --bin server -- -c qxbase.conf

# 2.clickhouse client连接
clickhouse-client --port 9528


#3. sudo权限下启动gdbgui， 非root权限可能导致无法attach上
sudo ./gdbgui_0.13.2.2

#4. 打开gdbui的web ui地址：http://127.0.0.1:5000/
# a.设置attach to process  pid为TensorBase的进程
# b.点击运行
# c. 打开文件crates/runtime/src/read.rs，设置点击行断点
#   该文件是处理查询逻辑
```

![](tensorbase笔记图片/Snipaste_2021-07-15_17-43-34.png)



### 4.1 SQL执行流程



- `crates/server/src/server.rs` 
  - 启动http服务器
- `crates/server/src/lib.rs` 
  - `runtime::ch::messages::response_to;` 打印结果
    - `response_query`
- `crates/runtime/src/mgmt.rs`
  - 读取配置文件，创建`BaseMgmtSys`服务
  - `BaseMgmtSys`实现了各种命令的处理
    - 创建、显示、删除数据库、表，desc 表，truncate 表
    - insert into 语句
    - query（select）语句
      - 先`parse_table_place` 解析表的位置，目前只支持local表
        - `READ`: `SyncOnceCell<T> ` 封装的读取方法，会跳转到`crates/runtime/src/read.rs`的`query`函数
          - `SyncOnceCell<T> `  rust lazy 初始化
    - 统一的入口是`run_commands` 方法
- `crates/runtime/src/read.rs`
  - `query`函数，执行`crates/engine/src/lib.rs`的`run`函数
    - `parse_tables`  `crates/lang/src/parse.rs` 解析表
    - `datafusions::run` 调用datafusion执行
      - `crates/datafusion/src/execution.context.rs` 的`sql`方法，执行SQL然后创建数据帧
        - `crates/datafusion/src/execution.context.rs`  `create_logical_plan` 创建逻辑计划
        - `crates/datafusion/src/execution.context.rs` 的`optimze`方法 做逻辑优化
        - `crates/datafusion/src/execution.context.rs`  `create_physical_plan` 创建物理计划



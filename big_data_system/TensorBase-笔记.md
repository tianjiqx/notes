# TensorBase-笔记

## 1. 背景

[TensorBase](https://github.com/tensorbase/tensorbase)用开源的文化和方式，重新构建一个Rust编写的实时数据仓库，用于海量数据的存储和分析。



优点：

- All in Rust
  - 借助rust语言的高性能(c/c++)，无GC，内存、线程安全性。
- ClickHouse协议兼容
  - 用Rust实现了一个高性能的ClickHouse SQL方言解析器和TCP通讯协议栈
  - ClickHouse TCP客户端可以无缝连接TensorBase
- 基于Apache arrow-rs，DataFousion获取高性能分析能力。
  - 柱状的内存数据格式
  - 数据交换Copy-free，Rust语言机制带来的Lock-free，Async-free，Dyn-free
  - 项目外依赖减少，以减少开发者重新编译时间



缺点：

- 还是起步的demo原型概念验证的阶段
  - 目前只是对于单表的聚合操作，相比clickhouse有明显的优势3X（并且数据完全加载进内存了，如果涉及磁盘读取，CH由于数据压缩，反而具有更好的性能，TB当前是原始数据）。

    



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

  - 基于DataFusion的Ballista，类ClickHouse的简易（半人工）分布式集群方案。

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
#（rust 编译确实太慢了，尝试支持multi statement，修改后，不清楚原理，有时依赖的公共包，依然需要重新编译）

# release 版本
cargo run --release --bin server -- -c crates/server/tests/confs/base.conf


# 连接
clickhouse-client --port 9528

# 推荐支持使用multi statement的参数
clickhouse-client --port 9528 -n

```

测试sql：

```sql
create table employees (id UInt64, salary UInt64) ENGINE = BaseStorage
insert into employees values (0, 1000), (1, 1500)
select count(id) from employees
select avg(salary) from employees


show tables employees


-- join 测试 ,注意，当前部分关键字（列类型）大小写敏感，和clickhouse行为一致

create table employeeNames (id UInt64, name String) ENGINE = BaseStorage
insert into employeeNames values (0, 'Tom'), (1, 'Jack')
insert into employeeNames values (2, 'Jame')


-- bug: client崩溃，Server也崩溃，Exception on client:
-- Code: 32. DB::Exception: Attempt to read after eof: while receiving packet from -- localhost:9528
-- select count(1) from employeesName



select count(id) from employeeNames

select * from  employeeNames

-- 必须加inner
--  employees.id  nvalid identifier '#employees.id' for schema employees.employees.id,


-- Code: 7. DB::Exception: Received from localhost:9528. WrappingEngineError(WrappingDFError(Plan("Ambiguous reference to field named 'id'"))). Error during planning: Ambiguous reference to field named 'id'.

-- select id,name,salary from employees inner join employeeNames on employees.id = employeeNames.id


-- Code: 7. DB::Exception: Received from localhost:9528. WrappingEngineError(WrappingDFError(Plan("Invalid identifier '#a.id' for schema a.salary, b.name"))). Error during planning: Invalid identifier '#a.id' for schema a.salary, b.name.

-- select a.id,name,salary from employees a inner join employeeNames b on a.id = b.id

-- Code: 7. DB::Exception: Received from localhost:9528. WrappingEngineError(WrappingDFError(Plan("Invalid identifier '#a.id' for schema a.salary, b.name"))). Error during planning: Invalid identifier '#a.id' for schema a.salary, b.name.

-- select name,salary from employees as a inner join employeeNames as b on a.id = b.id



-- Code: 7. DB::Exception: Received from localhost:9528. WrappingEngineError(WrappingDFError(Plan("Invalid identifier '#employees.id' for schema employees.salary, employees.employees.id, employeeNames.employeeNames.id, employeeNames.name"))). Error during planning: Invalid identifier '#employees.id' for schema employees.salary, employees.employees.id, employeeNames.employeeNames.id, employeeNames.name.

-- select name,salary from employees inner join employeeNames on employees.id = employeeNames.id

-- Code: 7. DB::Exception: Received from localhost:9528. WrappingEngineError(WrappingDFError(Plan("Ambiguous reference to field named 'id'"))). Error during planning: Ambiguous reference to field named 'id'.

-- select name,salary from employees inner join employeeNames on id = id

drop table employeeNames

create table employeeNames ( employeeId UInt64, name String) ENGINE = BaseStorage
insert into employeeNames values (0, 'Tom'), (1, 'Jack')
insert into employeeNames values (2, 'Jame')

insert into employeeNames values (3, null)


select count(employeeId) from employeeNames

select count(*) from employeeNames

-- 会将 name为null的统计，right？
select count(name) from employeeNames

-- 直接写null 插入的结果为''
select * from  employeeNames
select * from  employeeNames where name=''


-- 该语法目前本应不支持
insert into employeeNames(employeeId) values (4)

-- bug: 插入 NULL值后 查询卡死
select * from  employeeNames
select name from employeeNames


-- 成功
select employeeId from employeeNames 


select name,salary from employees inner join employeeNames on id = employeeId


select * from employees inner join employeeNames on id = employeeId
┌─id─┬─salary─┬─employeeId─┬─name─┐
│  1 │   1500 │          1 │ Jack │
└────┴────────┴────────────┴──────┘
┌─id─┬─salary─┬─employeeId─┬─name─┐
│  0 │   1000 │          0 │ Tom  │
└────┴────────┴────────────┴──────┘
2 rows in set. Elapsed: 0.015 sec. 
-- 展示没有融合数据在一起，是因为独立计算展示的吗？


select id,name,salary from employees inner join -- xxx ;
employeeNames on id = employeeId;

select id,name,salary from employees inner join employeeNames on id = employeeId



-- 测试有分区键的表
create table employees_partby_id (id UInt64, salary UInt64) ENGINE = BaseStorage PARTITION BY id
insert into employees_partby_id values (0, 1000), (1, 1500)
insert into employees_partby_id values (2, 1000), (3, 1500)
insert into employees_partby_id values (4, 1000), (5, 1500)
insert into employees_partby_id values (6, 1000), (7, 1500)

-- 观察到分区数等于id数

select count(id) from employees_partby_id
select avg(salary) from employees_partby_id


-- 其他
-- unit test中给出了一个分区表达式是 PARTITION BY mod(uuid, 100000)，预先分配10w个分区，根据uuid随机分配到任意分区。



-- 多语句执行
drop table if exists employees;
create table employees (id UInt64, salary UInt64) ENGINE = BaseStorage;
insert into employees values (0, 1000), (1, 1500);
select count(id) from employees;
select avg(salary) from employees;

-- git commit --amend --no-edit --signoff
```



## 4.  源码分析

环境配置：

IDEA2021.1 + rust 插件 



代码版本2021.07.15：

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
clickhouse-client --port 9528 -n


#3. sudo权限下启动gdbgui， 非root权限可能导致无法attach上
sudo ./gdbgui_0.13.2.2

#4. 打开gdbui的web ui地址：http://127.0.0.1:5000/
# a.设置attach to process  pid为TensorBase的进程
# b.点击运行
# c. 打开文件crates/runtime/src/read.rs，设置点击行断点， 使用clickhouse client执行查询SQL
#   该文件是处理查询逻辑



# 4.调试断点

b crates/runtime/src/mgmt.rs:655
b crates/runtime/src/mgmt.rs:1123
b crates/runtime/src/ch/messages.rs:182
b crates/runtime/src/ch/blocks.rs:353
b crates/runtime/src/ch/blocks.rs:299
b crates/runtime/src/ch/blocks.rs:600
b crates/runtime/src/ch/blocks.rs:622
b crates/runtime/src/ch/blocks.rs:681

b crates/runtime/src/ch/messages.rs:95
b crates/runtime/src/ch/messages.rs:139
```

![](tensorbase笔记图片/Snipaste_2021-07-15_17-43-34.png)



### 4.1 SQL执行流程

- `crates/server/src/server.rs` 
  
  - 读取配置信息
  - 初始化读`    READ.get_or_init(|| query);` 和写`WRITE.get_or_init(|| write_block);` 数据的方法
    - SyncOnceCell::new() 保证是全局唯一函数对象？
  - 启动http服务器
  
- `crates/server/src/lib.rs` 

  - `runtime::ch::messages::response_to;` 消息处理，读取read_buf，写查询结果到write_buf
  - response_to处理完毕，检查write_buf不为空时，将数据（例如查询结果）flush到目标流

- `runtime/src/ch/messages.rs` client消息处理逻辑

  - `response_to`  

    - `ClientCodes::Query`  查询类型消息，进入`response_query`处理逻辑

      - 核心进入`crates/runtime/src/mgmt.rs` 的`run_commands` 方法执行查询

        - `run_commands`  当前只处理一条语句，返回一个`BaseCommandKind`

          虽然语法解析器本身`BqlParser::parse(Rule::cmd_list, cmds)`支持解析出多条语句。
          
        - clickhouse client 通过-n参数可以支持多条sql语句执行，并且会自动切分query，最后输入到`run_commands`  的sql还是只有一条。（其他连接器，如jdbc？可能需要手动切分）

- `crates/runtime/src/mgmt.rs`

  - 读取配置文件，创建`BaseMgmtSys`服务
  - `BaseMgmtSys`实现了各种命令的在`run_commands` 方法处理
    - 创建、显示、删除数据库、表，desc 表，truncate 表
    - insert into 语句
      - `command_insert_into` insert 语句处理
        - `InsertIntoContext.parse`() 将`Pair<Rule>`中信息填进InsertIntoContext
        - `command_insert_into_gen_header`  ，插入数据表头header、空列填充进`Block`
          - `Block.encode_to()`
            - `Block.encode_body()`
              - `Column.encode()`
          - 暂时不支持部分列，个人测试ok，可能columns解析问题，不过读取异常
          - 根据建表的列顺序插入值
          - 会行转列格式，封装进Column   `runtime/ch/blocks.rs`
            - name 列名
            - BaseChunk 存储列数据（很类似Apache Arrow结构）
              - 类型
              - 大小
              - 字节数据
              - null值的数组Vec<u8>  ，bitmap
              - 偏移数组Vec<u32>
              - lc_dict_data 字典？ Vec<u8>
            - 每个cell的处理`parse_literal_as_bytes`
          - `crates/runtime/src/ch/messages.rs`  InsertFormatInline  发送header信息，进入StageKind::DataEODPInsertQuery状态，通过`consume_read_buf`
          - StageKind::DataPacket 处理待插入的values内容`crates/runtime/src/ch/messages.rs`
            - CH client 将插入的sql，分成了头和数据包
            - `process_data_blk` 读取数据buf
            - `blk.decode_from(bs)` 从byte buf生成`Block`
              - `BytesDecoder<Column>.decode_column` 解析列数据
                - `decode_to_column` 函数
                - 尤其注意，对于String类型，从CH客户端发送的，会有一个offset (变长存储)
            - 通过WRITE 对象写数据Block
        - `command_insert_into_select` select...insert into 语法处理
          - BaseCommandKind::Query 执行子查询
            - 注意会跳转到`runtime/src/ch/messages.rs` 的`response_query()` 方法处理
              - `crates/runtime/src/ch/blocks.rs` 的Block类的encode_to方法，将数据填充进`BytesMut` 类型的缓冲区（实际是BaseSrvConn的write_buf）中
                - `Column.encode()`  逐列编码
            - `StageKind::DataEODPInsertQuery` 
            - `StageKind::DataPacket`  insert into 处理数据包
              - `process_data_blk` 预处理数据（例如消息有压缩，则解压缩），"拷贝"到read缓冲区
                - 如果没有压缩，拷贝实际是切片
              - `blk.decode_from(bs)` 将数据解码为Block格式
              - WRITE 对象写数据Block
                - `write_block()` `crates/runtime/src/write.rs`
          - BaseCommandKind::InsertFormatSelectValue 将子查询结果插入数据库
    - query（select）语句
      - 先`parse_table_place` 解析表的位置，目前只支持local表
        - `READ`: `SyncOnceCell<T> ` 封装的读取方法，会跳转到`crates/runtime/src/read.rs`的`query`函数
          - `SyncOnceCell<T> `  rust lazy 初始化 同步原语。表是只能写一次
          - 类似的有WRITE

- `crates/runtime/src/read.rs`
  
  - `query`函数，执行`crates/engine/src/lib.rs`的`run`函数
    - `parse_tables`  `crates/lang/src/parse.rs` 解析表TablesContext
    - `datafusions::run` 调用datafusion执行
      - `crates/datafusion/src/execution.context.rs` 的`sql`方法，执行SQL然后创建数据帧
        - `crates/datafusion/src/execution.context.rs`  `create_logical_plan` 创建逻辑计划
        - `crates/datafusion/src/execution.context.rs` 的`optimze`方法 做逻辑优化
        - `crates/datafusion/src/execution.context.rs`  `create_physical_plan` 创建物理计划

### 4.2 模块解构

#### 4.2.1 元信息 `crates/meta`

- `MetaStore` 元信息存储对象 `crates/meta/src/store/sys.rs`
  - 磁盘物理路径`.../tb_schema/m0`
  - 使用到的库sled（雪橇）
    - 嵌入式数据库，类似BTreeMap功能，支持插入kv，点查询，前缀范围查询，当前四棵树（0，1，ts，cs），使用到lsm-tree？
    - 优势是无锁树，零拷贝读取
    - 0存储名字与id的映射，1存储名字(id与名字的映射，数据库，表，列名)， ts表示表信息，cs表列信息
      - 表信息： 建表脚本cr，引擎en，分区表达式pa，分区列pc，setting信息（大概类似属性，以se开头），存储时加上tid作为前缀拼成key( Vec<u8>类型)，value以字节方式存储
- `PartStore` `crates/meta/src/store/parts.rs`
  - Partition Tree分区树，存储和管理分区数据的元信息
  - Column Partition列分区信息`CoPaInfo`，简写Copa，列存，数据按列管理
    - 内存地址addr
      - TB使用`libc::mmap` 函数将分区列文件，映射到内存地址，用于后续的读数据
        - `crates/base/src/mmap.rs` 的`mm_file_ro`函数
    - 内存地址addr_om  字符串列内存地址？
    - 大小size: usize 行数
    - 字节大小len_in_bytes
  - 磁盘路径`.../tb_schema/p0`
  - `PartStore`当前也是四棵树（ps，pt，pr，l），加上 存储数据路径字符串数组（测试配置只有一个数据目录，如果有多个数据目录，会根据ptk散列，获取数据路径）
    - `tree_part_size`分区（行数）大小ps， tid,ptk  -  size， tid,ptk都是u64,part_size是usize （为writer）
    - `tree_parts`分区pt， cid,ptk -  siz_in_bytes: usize， Copa大小信息，即分区列的字节大小（专为reader，保证读写不需要加锁，能够读到的数据，是已经写好的）
    - `tree_prids`prid pr, 也是一份分区总行数， tid,ptk - part_size     usize 大小  （为reader）
    - `tree_locks`表锁l， tid - :IVec
  - 核心方法
    - `get_prid_int_ptk` 根据tid,ptk,reserved_len，CAS更新分区行数(tree_part_size)
      - 因此并行插入单个分区（文件），占位
    - `set_copa_size_int_ptk` 根据tid,ptk,part_size 更新行数。（insert覆盖，tree_prids）
      - 一个分区，插入全部完成后，再更新的行数，为reader读取
      - 如果后面支持事务，倒是可以回滚插入的行数
      - 检查到`engine/src/datafusions.rs` 会用`fill_copainfos_int_by_ptk_range` 用到了`tree_prids` 读取的行，或许这个表/树是为了不影响读写不用加锁？
    - `insert_copa_int_ptk` 插入cid,ptk - siz_in_bytes 更新分区列文件长度（字节） （tree_parts）
    - `get_copa_siz_in_bytes_int_ptk` 参数cid,ptk，获取分区列文件长度（tree_parts）
    - `get_part_dir` 获取分区的路径（用户配置的数据目录路径）
      - 直接散列，感觉配置后，导致无法再修改
    - `fill_copainfos_int_by_ptk_range` 填充`CoPaInfo` 信息，将文件地址，映射到内存，用于后续数据的读取
- `BaseMgmtSys`  系统信息提供对象
  - `crates/runtime/src/mgmt.rs`
  - 静态变量，`BMS`， lazy加载
  - 读取配置文件初始化
  - 持有`MetaStore`  和`PartStore`，分区表达式函数指针的映射？(tid -  :SyncPointer<u8>)，时区信息
    - 这块涉及到分区表达式的计算，用到ligthjit模块



#### 4.2.2 写数据

 `crates/runtime/src/write.rs`

- 入口`write_block`
  - `MetaStore.get_table_info_partition_cols()` 根据表id（tid_pc）获取分区键信息ptks（HashMap<u64, Vec<(u32, u32)>>类型）
    - 注意，建表时，未指定分区列时，直接创建`0, vec![(0, (blk.nrows - 1) as u32)]` 也就是只有一个分区ptk=0
  - `gen_parts_by_ptk_names` 创建一个分区的HashMap<u64, Vec<(u32, u32)>
    - 先根据分区列列名获取分区列索引ptk_idx 
      - （这里看起来只支持单列的分区，这里分区键是等同是主键？如果数据分区不是按内部自己增的rowid，而是按照真实数据主键列，那么对于事实表的分区划分，是否可能会导致数据分布不均？）
    - `BaseMgmtSys.get_ptk_exps_fn_ptr` 获取分区表达式函数指针
    - 根据列类型，转换原始Vec[u8]类型的数据为实际类型的字节数组`cdata_ptk`，如Vec[u16]，Vec[u32] 通过`gen_part_idxs`生成分区数据索引HashMap<u64, Vec<(u32, u32)>>
      - 对于Block的每一行，都会调用分区函数`ptk_expr_fn`计算所属的分区id（ptk）
      - key： ptk， `ptk_expr_fn(cdata_ptk[j]), j是行idx`， 根据下面value的填充，会多行共用，在根据后面写parts前，检查不能超过1000，应该是分区标识分区id， `ptk_expr_fn` 应该是一个分区函数，接收行号，转为分区id。这只是内存中，一次写Block的分区划分，Block大小，看注释，假定不能不超过4G。（更新：已确认ptk就是分区id，u64）
      - value： 元组数组Vec<(u32, u32)（插入该分区的行的范围的数组）
        - 第一次初始化（数组为空），push 元组(行号:u32，行号:u32)，
        - 第二次插入，条件匹配，如果是连续的（前一行也是插入到这个分区），修改元组(第一次行号:u32，第二次行号:u32)，插入前检查是否连续。闭区间。否者插入一个新的单行范围的元组，之后插入该分区的数据，使用最后一个元组重复次过程。
  - 循环迭代parts，调用`write_part/write_part_locked(有大字段类型，String)`  写分区数据（一个分区，实际一个文件，单线程，实际可以并行）
    - `PartStore.get_part_dir(ptk)` 获取分区数据目录(xxx/tb_data)
      - 配置多块数据目录时，可以将数据按分区散列到不同的目录
    - `ensure_table_path_existed` 确保分区路径存在，创建目录
    - `PartStore.acquire_lock(tid)?`  加表锁
      - 很简单，死循环尝试加锁
      - 注意，`tree_locks` 表锁树，每次重启时会clear，用于处理遗留的锁
    - `PartStore.get_prid_int_ptk(tid, ptk, pt_len)` ， pt_len为此次插入的分区行数(Vec<(u32, u32)>范围求和) 获取已写的分区行数，并更新（先占位，后续才实际写）
      - `PartStore.tree_part_size.fetch_and_update()` 会从分区元信息中获取旧的分区行数，加上pt_len
    - 逐列，插入数据
      - `get_part_path(tid, cid, ptk, dp)` 获取分区路径 
        - 表单独一级目录
        - 列id_分区ptk 作为一个文件名 例子：`tmp/tb_data/6000006/6000007_0,tmp/tb_data/6000006/6000008_0`
      - `open_file_as_fd` 根据路径名打开文件描述符
      - `gather_into_buf` 拷贝数据到缓冲区，合并Vec<(u32, u32)>的数据
        - 循环`copy_nonoverlapping`,虽然是个循环，但以目前看只有一个元组
      - `dump_buf()`  刷数据到文件（fd，文件偏移量，长度，buf），落盘
        - `libc::fallocate()`
        - `libc::pwrite()`
        - `libc::close()`
        - 对于字符串列，会额外增加一个_om的列文件，dump_buf两次
          - om是offset_map简写，设计来自CH协议
        - 文件偏移offset_in_bytes=prid * ctyp_siz;
          - prid 表示总行数，ctyp_siz为定长大小的列类型（数据没有压缩）
      - `PartStore.release_lock(tid)` 释放表锁
        - 实际就是覆盖写0
      - `PartStore.insert_copa_int_ptk`  更新分区列文件字节大小（tree_parts）
    - `PartStore.set_copa_size_int_ptk` 更新分区行数（tree_prids）

**总结**：

TB写数据的文件组织设计，目前非压缩，最大的级别单位是Block，Block下面分成Part，分区可以根据配置，写到不同的目录（不同磁盘ok，节点？如下图的tb_data），分区下面是表级目录（id，如2000000），表级目录下面是一个个该分区的列文件（2000001_0，构成tid，列id，下划线，分区键（或者id）ptk，如果在同一个目录下，不同分区的分区列文件应该形如`2000001_1`）。om文件目前是String列的数据。



![](tensorbase笔记图片/Snipaste_2021-07-20_16-53-08.png)

插入数据的时候，未设置分区键，将只有一个分区，一直追加分区列文件。

- `tree_part_size` 记录了每个分区列文件的行数，用于计算分区列文件的大小
  - `get_prid_int_ptk` 在落盘前获取并CAS更新表分区行数`tree_part_size` 
  - 之后逐列追加分区列文件数据
  - 根据行数prid和列类型大小，计算出分区列文件的起始偏移
    - 这里的偏移地址，为什么不用`tree_parts` 中的地址呢？这才是真实落盘的大小，如果写文件突然被kill，下次获取prid将不正确，暂时没有看到有修正此prid机制
      - 或许可以考虑，`tree_prids` 中表分区的行数，修正`tree_part_size`中的行数。手动运维判断？
  - `insert_copa_int_ptk` 在所有的分区列文件数据完成落盘后，更新`tree_prids` 中表分区的行数
- `tree_parts` 存储每个分区列文件的当前大小
  - 分区列文件数据落盘后更新
    - insert方式，如果并发写一个分区列文件，可能导致大小不正确，不过有加锁机制，保证获取到的位置是正确的，并且单线程写分区列文件
  - 所以这里其实可以忽略插入失败情况，应该是先插入数据后更新行数？
    - `insert_copa_int_ptk` 是在每个分区列文件落盘后更新文件大小

在TB的架构设计说明：

> 在存储层，TensorBase非经典的列式存储。这其中最重要的，我们给出了一个反重力设计：No LSM。我们不再使用在目前开源数据库及大数据平台流行的LSM Tree（Log Structured Merge Tree）数据结构。而是使用一种我们自己称之为Partition Tree的数据结构，数据直接写入分区文件，在保持append only写入性能的同时，避免了LSM结构的后续compact开销。得益于现代Linux内核的支持和巧妙的写入设计，我们在用户态（User-space）核心读写链路上不使用任何锁（Lock-free），最大程度的发挥了高并发网络服务层所提供的能力，可以提供超高速数据写入服务。

当前不支持update，delete操作，也没有唯一主键。适用于一次性写，然后分析。

后续，可能考虑存储引擎，类似CH，折叠树。在计算引擎层，做数据的合并。

**无序**：

TB当前的这一个存储引擎`BaseStorage`不维持主键顺序，也没有什么排序键，单个分区文件也不会保证有序，看起来还是非常的原生态。插入友好。但是没有任何索引，应该对点查询不够友好（本身OLAP，点查询到不是重点），但是缺少文件的统计信息，索引文件，没办法做任何的过滤，减少读取的磁盘数据，需要在内存中做过滤。更适合面向中小数据规模的全内存分析。（RAMCloud）

**没有压缩**:

作为一个列存数据库，但是并没有如其他列存数据库，对列进行压缩。列存由于数据类型相同，其实可以获得很高压缩比例，减少磁盘存储空间，更重要的是能够减少读取磁盘的大小，IO总是很昂贵的。对于压缩的效率，根实际列类型的特点有关，提升数十倍也不稀奇。根据经验，以某列存数据的tpc-ds 1T的实际单副本的存储大小是442GB（使用的snappy），可知在通用的负载情况下，总的压缩比例也可以超过一半。根据最早的C-Store'05论文，TPC-H的数据集，只有40%的空间，也能验证这个数据是相对合理的。

据TB作者介绍考量，压缩除了是一种CPU和IO之间的tradeoff，牺牲CPU资源外，压缩算法（特指通用的，如LZ4，ZSTD，GZIP，snappy等）本身的解压速度就是一种对带宽瓶颈的限制，无法再提升性能。查看最近阿里云的云服务器ECS，最高可选的内网带宽最高可以达到32Gbps（4GB/s）。TB测试环境6-channel DDR4-2400 ECC REG 192GB DRAMs的内存带宽为（6\*2400\*64/8 MB/s= 6 \* 19200 MB/s = 6 * 18.75 GB = 112.5 GB/s）。在加载进内存，TB省略掉解压缩后，可以在内存接近内存带宽的比例进行数据处理。

[clickhouse使用通用和时序的压缩算法](https://developer.aliyun.com/article/780586)

[通用数据库压缩算法评估'2016](https://www.percona.com/blog/2016/04/13/evaluating-database-compression-methods-update/) 解压速度最快的LZ4，解压速度3130MB/s，是打不满网络带宽。（在做hdfs导入导出性能优化时，确实也发现这样的问题，一方面解压缩只能单线程做，CPU吃到100%，也压不满10Gb/s网络，另一方面，无法再使用FileChanel绕过内核与用户态之间的数据拷贝，因为必须cpu解压缩，进行零拷贝的数据传输。所以在有在千M网情况下，为了使用压缩才比较有优势）

（但是我认为对于使用字典压缩，和一些其他高级压缩，如前缀编码，运行长度编码 (RLE)，位图编码，解压速度应该不会是一个瓶颈，反而应该是能更快的提高计算性能，因为部分甚至是支持直接压缩读，已经直接通过压缩数据进行计算，如join等操作，详见[slide](https://github.com/tianjiqx/slides/blob/master/column-store-tutorial.pdf)；[SAP HANA 支持增量合并时进行压缩优化](https://help.sap.com/viewer/6a504812672d48ba865f4f4b268a881e/Cloud/en-US/bd9017c8bb571014ae79efaeb46940f3.html)）



`BaseStorage` 在磁盘上的格式，也是加载进内存后的格式（内存中的表示`CoPaInfo`）。（使用内存映射mmp加载数据）

TB利用的Apache Arrow格式，实际上支持字典编码，压缩数据。

不过，考虑未来可以增加其他更复杂引擎，适应其他负载。（存储引擎层都还未成为独立的模块），

或者支持直接读写CH的存储文件能够扩展更多的应用场景。



#### 4.2.3 读数据

 `crates/runtime/src/read.rs`

- `query()` 入口
  - 调用`crates/engine/src/lib.rs`的`run`函数
    - `parse_tables`  `crates/lang/src/parse.rs` 解析表TablesContext
    - 
    - `datafusions::run` 调用datafusion执行（`crates/engine/src/datafusions.rs`）
      - `crates/engine/src/datafusions.rs`
        - `setup_tables`  将TB的表信息、数据注册到DataFusion，作为内存表使用
          - `gen_arrow_arraydata`生成 arrow格式的数据
      - `crates/datafusion/src/execution/context.rs` 的`sql()`方法，执行原始SQL然后创建数据帧
        -  `create_logical_plan` 创建逻辑计划
          - `DFParser::parse_sql(sql)` 解析sql成DFStatement
          - `SqlToRel.statement_to_plan(&statements[0])`  处理DFStatement，转成逻辑计划
            - `DFStatement::CreateExternalTable` 外表
            - `DFStatement::Statement` 标准SQL语句->`sql_statement_to_plan()`
              - `Statement::Query` ->  `query_to_plan()` 
                - `crates/datafusion/src/sql/planner.rs`
                  - `crates/datafusion/src/sql/planner.rs` `create_relation` 创建relation 算子 LogicalPlan::TableScan
        -  `optimze`方法 做逻辑优化
          - 逐一应用逻辑优化规则`OptimizerRule`
        - 创建`DataFrame` 结构df，封装了逻辑计划
          - `DataFrame`  本身还是一个逻辑计划
        - `crates/engine/src/datafusions.rs` `df.collect().await` 创建物理计划，并执行，异步等待结果Vec<RecordBath>
          - `crates/datafusion/src/execution/context.rs``create_physical_plan` 创建物理计划
            - `PhysicalOptimizerRule` 物理优化规则
          - `crates/datafusion/src/physical_plan/mod.rs` 异步函数`collect()` 执行计划
            - 这里会根据数据是否被分区（datafusion的分区概念）包装plan一个`MergeExec` 算子，合并多个结果到一个单分区
              - `plan.execute(0).await` 调用物理计划的`execute` 方法
                - 顶层物理算子，递归拉去下层算子的输入流进行处理。
                  - `crates/datafusion/src/physical_plan/hash_join.rs` hashJoin 算子
                  - `crates/datafusion/src/physical_plan/filter.rs` filter 算子，批量过滤
                  - `crates/datafusion/src/physical_plan/source.rs` source 算子，数据源
                    - `crates/datafusion/src/datasource/memory.rs` TB使用MemTable 作为数据源类型 `scan`
  - 将查询的结果放进Vec<Block> 中返回。
    - `Block::try_from()`  `crates/runtime/src/ch/blocks.rs` 转换arrow格式的`RecordBatch` 为`Block`



总结：

TensorBase的读数据的流程，实际上自身先解析一次sql，获取表信息，需要投影的列，然后将参与的表全部加载进内存，作为datafusion的数据源。datafusion会再次解析sql，完成诸如 filter，join等逻辑，数据源来自于之前setup进内存的表。

对于这种提供数据源的方式，需要将数据完全加载进内存才行，后续其实可以提供，类似datafusion自己带的csv，parquet文件格式的读取。

优势，

- 可以分布式读取数据源，
- ~~可以pipeline，不必等待数据完全加载进内存后才能进行后续处理。~~
  - 数据注册过程，根据沟通，只是做磁盘文件与内存的映射，并不真正加载数据，所以不会暂停
- 重用查询优化，不必自己重写一套分区裁剪等逻辑减少读取的数据。并且后续能够基于真实代价模型，调整执行计划。



### 4.3 DataFusion

TensorBase的SQL 查询语句的执行引擎，绝大部分工作的承担者是Apache Arrow DataFusion。

架构、原理相关，可以参考[Apache arrow笔记](https://github.com/tianjiqx/notes/blob/master/big_data_system/Apache%20Arrow.md)

#### 4.3.1 ExecutionContext

`crates/datafusion/src/execution/context.rs`

执行上下文，用来注册数据源和执行查询。

- 注册数据源
  - `register_table` 方法，TB使用该方法将TB自己引擎的表，注册成内存表类型的数据源，供DataFusion后续处理。
    - 数据源类型，由`TableProvider` trait提供，`MemTable` 实现了该trait
      - `crates/datafusion/src/datasource/memory.rs` 
      - MemTable中包含
        - SchemaRef
        - Vec<Vec<RecordBatch>>，外层Vec表示partition的集合，内存Vec表示一个分区有多个RecordBatch构成，一个RecordBatch表示一定行数的列存格式记录的集合。
        - 表统计信息
          - 表的行数，字节数，列的统计信息（null值，min，max，ndv）
    - `TableProvider` 方法
  - `register_csv` 注册CSV数据源（表名，文件路径）
  - `register_parquet` 注册Parquet数据源（表名，文件路径）
    - `crates/datafusion/src/physical_plan/parquet.rs` 文件定义了 `ParquetExec`  查询本地目录下所有的parquet格式文件，这里暂时不支持如hadoop等存储引擎上的文件。（也无副本可以用）
      - 已经有一个rust访问hdfs集群的包https://github.com/hyunsik/hdfs-rs.git 不过已经是2015 年，很久未更新。另一个近期的是https://github.com/frqc/rust-hdfs  2020 年
      - hadoop官方另外了一种访问方式是webHDFS
      - path是简单的一个字符串类型，在`ParquetExec.try_from_path` 方法中创建读取本地目录路径下的parquet文件的物理执行计划。（若在ballista的分不会是计划情况下，需要executor路径一致？）
  - `register_udaf` 和`register_udf` 注册聚集UDF和标量UDF
  - `register_catalog` 注册catlog信息，包含一系列schema。
    - `CatalogProvider`
      - `SchemaProvider`
  - 注册变量等
  
- 执行`sql()`，创建一个DataFrame，df.colletion() 触发物理计划生成和执行。
  - 包含创建逻辑计划，逻辑优化，物理计划。
    - `crates/datafusion/src/sql`  
      - `parser.rc`词法，语法解析成Statement
      - `planner.rs` 逻辑计划生成
    - `crates/datafusion/src/logical_plan` 
    - `crates/datafusion/src/optimizer`
    - `crates/datafusion/src/physical_plan`  
    - `crates/datafusion/src/physical_optimizer`  

#### 4.3.2 向量化执行

在datafusion中，充分使用向量化的方式，批处理记录。

- 表达式的向量化处理
  - `crates/datafusion/src/physical_plan/expressions`
  - `CountAccumulator`  count表达式的累加器
    - `update_batch()` 方法接受数组，计算并增加非null值的个数
    - `merge_batch()` 方法接受数组，计算并增加行数（包括null）
    - `evaluate` 方法返回当前总行数
  - `MaxAccumulator` max表达式累加器
    - `update_batch()` 方法接受数组，计算这批数据的最大值`max_batch`，然后与当前累加器中最大值比较替换
    - `merge_batch()` 方法接受数组，调用update_batch方法
    - `evaluate` 方法当前最大值
  - `impl PhysicalExpr for Column` 
    - `evaluate` 方法 返回一列的一批数据`ColumnarValue` 
      - Array 列值的数组
      - Scalar 单个标量值， `into_array` 方法将单个标量转成一个具有相同值的数组
        - 即类似filter  c1=10 的时候，会将Literal类型10的标量值，先转成10的数组，c1读取该列的数据，然后进行BinaryExpr的计算。

- 算子的向量化处理
  - GroupBy、Distinct
    - `crates/datafusion/src/physical_plan/hash_aggregate.rs`
    - `HashAggregateExec` DataFusion的group by实现方式，使用hash进行分组
    - GroupedHashAggregateStream 将一个数据流转换为一个以hash分组，并聚合结果的流
      - 输入和输出的next都是RecordBatch对象
    - 对给定的一批记录RecordBatch进行处理`group_aggregate_batch`
      - `evaluate` 获取待group列的数据
      - `evaluate_many` 获取聚合列的数据
      - 初始化分组key，聚合累加器
      - 迭代每一行，检查key是否存在，不存在插入map，存在追加map项值的数组中
        - `GroupByScalar` 单个key的分组表示
      - 迭代没一个key，调用CountAccumulator 计算聚合的结果
    - 迭代完所有RecordBatch后，根据聚合累加器中的结果生成输出RecordBatch`create_batch_from_map`
  - Join
    - `crates/datafusion/src/physical_plan/hash_aggregate.rs`
    - `HashJoinExec` datafusion的join，实现方式也是hash join算法
      - 合并left 的输入成一个流
      - 迭代流的每一个RecordBatch，更新hash表
      - 完成后，由hash表生成一个新的RecordBatch
        - 看起来，需要满足left表能够完全装进内存
      - 构建HashJoinStream
        - `poll_next` 迭代处理right流的RecordBatch

### 4.4 Ballista

Ballista是DataFusion的分布式扩展，类Spark的执行引擎，已经合并进datafusion，概要的介绍，也可以参考[Apache arrow笔记](https://github.com/tianjiqx/notes/blob/master/big_data_system/Apache%20Arrow.md)。

主要的组件：

- 调度器Scheduler
- 执行器Executor
- 客户端Client

（PS1：目前似乎没有看到TB使用Ballista，而是直接使用Datafusion，应该还是单机模式，毕竟注册的数据源还内存表）

（PS2：根据早前2019info翻译了一篇文章有人用rust重写了spark，现在叫[vega](https://github.com/rajasekarv/vega) 现在作者似乎断断续续的还在开发） 

#### 4.4.1 调度器Scheduler

调度器实现了rRPC接口，提供以下方法

- ExecuteQuery 
  - 提交逻辑执行计划，或SQL，用于执行
- GetExecutorsMetadata 
  - 返回注册到调度器上的执行器信息
- GetFileMetadata
  - 返回整个集群中可用的文件元信息
- GetJobStatus
  - 返回已经提交的查询的状态
- RegisterExecutor
  - 注册执行器到调度器

调度器可以以单点standalone方式运行，也可以使用etcd存储状态以集群模式运行。



**源码:**

- main函数
  - `crates/ballista/rust/scheduler/src/main.rs`
  - 读取配置文件（etcd/sled）
  - 启动调度器服务SchedulerServer
- SchedulerServer
  - `crates/ballista/rust/scheduler/src/lib.rs`
  - SchedulerGrpc 接口的方法
    - `execute_query` 处理提交逻辑执行计划、SQL
      - 解析逻辑计划，或者SQL
      - 创建并保存job信息
      - 独立线程，使用DataFusion创建物理计划，优化
      - 更新job状态
      - 使用`DistributedPlanner.plan_query_stages`  做分布式计划 query stage的生成
      - 保存query stages 到任务队列
      - 返回job id给客户端
    - `get_file_metadata` 处理获取文件元信息
    - `get_job_status` 处理获取任务状态请求
    - `poll_work`  处理执行器Executor请求（task执行完，请求更新任务状态，是否可以接受新的task，如果可以，返回一个新的task给执行器）
  - SchedulerState  调度器存储的状态，如任务状态信息，executor元信息等
    - `crates/ballista/rust/scheduler/src/state/mod.rs`
  - DistributedPlanner 将物理计划，划分为多个stages，stage的输出结果需要落盘
    - `crates/ballista/rust/scheduler/src/planner.rs`
    - `plan_query_stages`



#### 4.4.2 执行器Executor

执行器实现了Apache Arrow Filinght gRPC接口，负责

- 执行查询stage，以apache arrow IPC格式持久化结果到磁盘
- 将查询阶段结果作为 Flights 提供，以便其他执行程序和客户端可以检索它们



**源码:**

- mian函数
  - `crates/ballista/rust/executor/src/main.rs`
  - 读取配置文件
  - 创建Executor，BallistaFlightService，FlightServiceServer对象
    - FlightServiceServer封装BallistaFlightService，BallistaFlightService封装executor
  - 启动FlightServiceServer服务
  - 调度器gprc client连接到调度器，独立线程周期性的注册自己的元信息（心跳）
- Executor
  - `execute_partition` 执行一个query stage的一个分区处理，以apache arrow IPC格式持久化结果到磁盘，返回一个RecordBatch
    - `QueryStageExec::try_new` 创建执行者
    - `QueryStageExec.execute` 执行，返回结果流（RecordBatchStream，可以包含多个RecordBatch）
      - `crates/ballista/rust/core/src/execution_plans/query_stage.rs`
      - 调用物理执行计划的`execute`方法
      - 执行结果的处理
        - 不需要shuffle输出
          - `utils::write_stream_to_disk` 将结果写到磁盘
            - 一个stages可以包含多个执行算子（类似如spark一个窄依赖，划分的stage）
          - 封装流结果为单RecordBatch的MemoryStream
        - 需要
          - 迭代处理每个RecordBatch的没一行，散列，生成索引信息，最后每个writer（等于输出分区个数），根据索引信息，以RecordBatch为粒度，写磁盘。
          - 封装流分区的元信息（如路径）为单RecordBatch的MemoryStream
    - `utils::collect_stream` 将结果流转换为RecordBatch（实际就简单从流提取一个RecordBatch）
- FlightServiceServer
  - 提供query stage的结果数据查询检索服务
  - 标准方法`do_get`,`do_put`等



#### 4.4.3 客户端Client

Rust 客户端提供了一个 DataFrame API，它是 DataFusion DataFrame 的瘦包装器，并为客户端提供了构建执行查询计划的方法。

客户端通过提交`ExecuteLogicalPlan`到调度器来执行查询计划，然后调用 `GetJobStatus`以检查是否完成。

完成后，客户端会收到包含查询结果的 Flights 位置列表，然后将连接到适当的执行器进程以检索这些结果。



**源码:**

- `BallistaContext`
  - `crates/ballista/rust/client/src/context.rs`
  - 远程Ballista调度程序实例执行查询的上下文
    - 唯一成员`state: Arc<Mutex<BallistaContextState>>`
      - `BallistaContextState` 包含调度器的主机ip，端口，已经注册的表
    - 提供如`read_parquet`方法，创建表扫描的DataFrame。
      - `create_datafusion_context` 调用datafusion的方法创建datafusion的`ExecutionContext`
      - 使用datafusion的`ExecutionContext.read_parquet`  方法创建DataFrame
    - `register_parquet` 将读取到的DF，注册到`BallistaContext`，以便后续使用
  - `sql` 接受sql，返回DF（逻辑计划）
  - `collect` 执行sql，连接调度器后
    - `execute_query` 生成job
    - 循环检查job状态
      - Executor会死循环向Scheduler拉去任务`poll_work`，执行完毕后更新任务状态
    - 发现job 完成后，收集所有分区的结果，返回RecordBatchStream



#### 4.4.5 分布式执行计划

Ballista的分布式执行计划实现，非常类似于SparkSQL的执行机制。

有jobid，stageid的DAG图划分，以及通过ShuffleWriterExec和ShuffleReaderExec算子完成，数据的重分布。

- DistributedPlanner

  - `crates/ballista/rust/scheduler/src/planner.rs`
  - `plan_query_stages`分布式计划的生成
    - `plan_query_stages_internal` 将原单机的执行计划，转为分布式的执行计划，返回执行计划和stages的数组，一个stage是一个ShuffleWriterExec。
      - 是一个递归的算法
      - 从根节点开始，遍历孩子节点，将孩子节点应用`plan_query_stages_internal`生成新的执行计划孩子和孩子对应的stages，将孩子的stages追加到本节点需要返回的stages中
      - 各个逻辑算子的处理
        - `DfTableAdapter`  表示一个数据源
          - 返回（生成物理计划，孩子节点的stages）
        - `CoalescePartitionsExec` 折叠所有分区成一个单分区
          - 创建一个stage（ShuffleWriterExec），并添加到需要返回的stages中
            - ShuffleWriterExec的孩子计划是CoalescePartitionsExec的孩子计划，单分区（即分区类型None）
        - `RepartitionExec` 数据重分区/重分布
          - 创建一个stage（ShuffleWriterExec），并添加到需要返回的stages中
            - ShuffleWriterExec的孩子计划是RepartitionExec的孩子计划，分区方法是RepartitionExec的分区方法
        - `WindowAggExec` 窗口函数
          - 未实现，保存
        - 其他
          - 返回（替换了孩子节点的执行计划，孩子节点的stages）
    - `create_shuffle_writer`
      - 创建一个`ShuffleWriterExec` 算子，输出单个分区，作为最终的query stage，输出查询结果。
  - `remove_unresolved_shuffles` 事实上在`plan_query_stages` 生成的计划并不完整，缺乏真正shuffle结果的路径信息（因为还未调度，无法知道真正的执行节点），在创建ShuffleWriterExec时，使用UnresolvedShuffleExec进行了包装。
    - 调度器，在调度计划时，会在`assign_next_schedulable_task` 方法中处理，使用ShuffleReaderExec替换，设置上一个stage，shuffle完后的真正的路径信息。
- ShuffleWriterExec
  - `crates/ballista/rust/core/src/execution_plans/shuffle_writer.rs`
  - 查询计划的一个部分section，该部分具有一致的分区，作为一个单元执行，每个分区并行执行。 每个分区的输出被重新分区并以 Arrow IPC 格式流式传输到磁盘。 查询的后续阶段将使用 ShuffleReaderExec 来读取这些结果。还有一个用于延迟计算的UnresolvedShuffleExec的包装器类。
  - 单孩子节点（上层的执行计划）
  - 执行`execute`，处理单个分区
    - 调用孩子的执行计划，处理该分区，返回一个SendableRecordBatchStream
    - shuffle输出类型
      - 单一分区，不分区（None）
        - 直接将孩子的输出流写到磁盘（work_dir/job_id/stage_id/partition）`utils::write_stream_to_disk`
          - 异步的方法
        - 返回MemoryStream，包含一个RecordBatch，RecordBatch中保存有分区文件路径信息，统计信息。
      - hash分区 （**列存格式的数据散列**）
        - 根据hash后的分区数量，创建对应数量的ShuffleWriter（实际使用时，没有再创建一次）
        - 遍历读取孩子的输出流的每个RecordBatch
          - 根据hash的表达式（可能复数个列），计算结果`Vec<ArrayRef>`类型，`ArrayRef` 长度为batch的长度
          - `datafusion::physical_plan::hash_join::create_hashes`  函数，联合多列的hash表达式计算结果，对每行生成一个hash值（如果只有一列，那么就是之前计算的hash值）。
          - 对每个hash值，根据分区个数，散列，计算所属的索引数组位置
            - `*hash % num_output_partitions as u64`
          - 遍历索引数组
            - 根据索引，逐列提取需要输出到某个分区的值（指针，引用计数，非内存数据拷贝，fine）
              - （这里可能可以优化，如果索引集合为空可以直接continue）
            - 封装colmns数据为RecordBatch
            - 通过ShuffleWriter，写RecordBatch到目标路径
            - （可能看到性能跟hash结果的分区数量以及一行包含的列的个数有关，一个RecordBatch包含的行数应该远大于分区数量才比较好，如果相等，理论上性能应该是接近行存的散列）
              - 散列后的分区数量，一般应该接近executor的个数，而RecordBatch一般应该设置超过1000行，这样一看，列存格式的shuffle，理论上性能应该不成问题（之前以为会有内存拷贝，需要重新组织列存格式）
              - 对于小数据集，会更加适合广播hash join。
- ShuffleReaderExec
  - `crates/ballista/rust/core/src/execution_plans/shuffle_reader.rs`
  - 读取已经被executor执行的ShuffleWriterExec物化到磁盘的分区
  - 无孩子节点
  - 分区`partition: Vec<Vec<PartitionLocation>>`
    - `partition[i]` 表示单个分区是`Vec<PartitionLocation>`类型，`PartitionLocation`的数组，即reader上的一个分区，会收集各个executor上的属于该分区的数据。
      - `PartitionLocation` 表示一个执行器上的一个分区。
        - `PartitionId` 分区id
        - `ExecutorMeta` 执行器的元信息（id，host，port）
        - `PartitionStats` 分区的统计信息（行数，batch数，字节数）
  - 执行（读取单个分区数据）
    - 遍历``partition[i]` 中的分区数据位置
      - 通过`BallistaClient.fetch_partition` 方法想每个executor拉取数据
    - 合并成一个输出流`RecordBatchStream`



简单的想法：

- ballista 作为计算引擎层，TB实例作为存储引擎节点，算作一种计算与存储分离的架构。与spark外接各种存储引擎的模式类似。更多，spark可以部署在yarn或者k8s（后者看起来更前途光明）上，ballista 也可以类似。

- ballista 获取数据源，以当前datafusion的注册数据源的方式，在client端注册数据源信息，生成逻辑计划，然后提交计划到scheduler进行执行。

  datafusion的注册数据源接口还很简单。可以参考Spark DataSource/DataSource V2 接口注册数据源，下推的filter。

- TB 当前自己的原信息存储在sled中，当前是单机版本。可以提取出来，以etcd？管理的sled集群，提供元信息服务。这样的设计变成hive的metastore角色、tidb的PD cluster。实际还是单点服务，有其他的可扩展、高可用思路吗？（k8s来管理？todo学习k8s架构原理，k8s operator）元信息管理的负载情况 （clickhouse的元信息管理？）

  元信息管理，与ballista  scheduler是同样的master类似的角色，但是不合并在一起的理由：模块解耦，可更换、外接计算引擎（spark，kylin等），接hadoop生态。

  提供元信息接口，meta client，供datafusio使用的另外好处，在4.2.3 节总结提到。

- 关于WAL，对于OLAP系统来讲个人未了解相关实现（hbase WAL算？），如hive，是没有的，而是写进临时目录，来保证原子性。（todo：读有些重新思考数据库的架构论文，对日志是如何考虑的。aurora 这个OLTP对日志的优化，polardb对日志的优化）对大数据，OLAP系统而言，特点是大数据批量插入，非单条写入。从集中是数据库，引入日志，是为了保证单机崩溃，用redo，undo处理脏页的问题，分布式数据库，利用日志和raft等算法，可以进行副本状态机一致性的改变。对TB的base引擎，数据文件特点是是追加的，是否完全可以不需要考虑脏页问题，保证文件offset正确，只需要覆盖即可？不过存在日志的一个额外好处是，对于扩展系统如备份，恢复、同步，可以拷贝日志，保证实时性和事务一致性状态的恢复。如果只有记录数据的物理文件，如果是物理文件为单位备份恢复，实时性无法保证。（考虑数据即日志？）（tidb似乎有从tiflash写tikv的路径，如何做日志同步的）



## REEF

- [TensorBase](https://github.com/tensorbase/tensorbase)
- [开源产品 | TensorBase，基于Rust的现代化开源数据仓库](https://rustmagazine.github.io/rust_magazine_2021/chapter_4/tensorbase.html)


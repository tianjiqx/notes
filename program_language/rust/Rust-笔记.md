# Rust-笔记

[TOC]



## 1. 背景

### 1.1 简介

一门赋予每个人构建**可靠**且**高效**软件能力的语言。

关键词：无GC且能保证内存安全、并发安全和高性能。

> 发展历史：
>
> 2008年开始由
> Graydon Hoare 私⼈研发，2009年得到 Mozilla 赞助，2010年⾸次发布 0.1.0 版本。2015年5⽉15号发布 1.0 版本。
>
> 2021年 2 ⽉ 9 号，Rust 基⾦会宣布成⽴。华为、AWS、Google、微软、Mozilla、Facebook 等科技⾏业领军巨头加⼊ Rust 基⾦会，成为⽩⾦成员，以致⼒于在全球范围内推⼴和发展 Rust 语⾔。  



#### 1.1.2 Rust优势

- 高性能
  - 运行速度快，C/C++级别
  - 内存利用率极高，也是C/C++ 级别（比java，go有极大优势，Andy Grove在测试rust编写的[datafusion与spark对比](https://andygrove.io/rust_bigdata_benchmarks/)，需要的内存分别是128MB，1GB）
- 可靠性、安全
  - Rust 使编写不安全的代码变得困难。
    - 丰富的类型系统和所有权模型保证了**内存安全**和**线程安全**，编译期，消除各种错误。
  - 静态管理内存
  - 借用检查（borrow checking）
    - 每次传递一个变量（即对存储位置的引用）时，都必须指定引用是可变的（mutable）还是不可变（immutable）的
      - 编译器会使用一系列规则，来确保不能同时在两个位置上更改同一个内存区域，**无数据竞争**
- 开发效率
  - 文档，友好的编译器和清晰的错误提示信息，开发者社区
  -  包管理器和构建工具
  - 编辑器支持，智能地自动补全和类型检验， 以及自动格式化代码

Rust足够底层，如果有必要，它可以像 C ⼀样进行优化，以实现最高性能。（SIMD？）

比C，更容易并行化代码。

支持持异步编程的系统级语言。（async/awit）



### 1.2 与其他语言对比

（很可能有过时信息）

#### 1.2.1 rust 与go对比

**go优势：**

- 编译时间，可能略快于C/C++
- 学习简单
- **协程（goroutine）和信道（channel）**，轻量级语法，并发编程效率
- 隐式接口，增加实现，无需显式声明。（但是也让人不好找具体实现）
- GC，支持可变参数
- 工具链友好

**go缺点：**

- 缺少泛型和宏，写冗余代码，只是类型不同

**rust与go相似处**：

- 介于偏底层的系统语言（就像 C 或 C++ 语言）和基于运行时的语言（比如 Java 或 Python）之间，适用于系统编程领域
- 易于部署/分发和方便交叉编译
- 解决高性能或高并发的问题
  - rust：CPU+内存密集型的应用，比如数据压缩领域的gzip、bzip2、xz
- 内存管理，策略不同，但是同时稳固、可靠、易于维护和升级

**rust与go差异：**

- 并发
  - Go 具有 goroutine+channel 的并发模型
    - 绿色线程
  - Rust 朝 Future 模型发展， async/await 模型，以同步的方式和思维编写代码，但以异步方式执行。
    - 零成本抽象（未使用不承担额外开销），
      - 很多抽象实现，实际是编译器帮你翻译了代码实现
        - [Rust适合用来写linux内核模块吗？](https://zhuanlan.zhihu.com/p/137907908)
- 性能
  - Rust核心库有SIMD优化过的库，go需要编写调用的汇编
- 泛型
  - go缺失，Rust 具有强大的类型系统并支持泛型。
  - Rust 还有一个功能非常强大的宏（macro）系统，可以使编译器做很多工作，比如生成代码，除此之外还有更多可以细粒度控制的细节。
- 发布周期
  - Rust 的发布周期：更加透明，周期明确，开源项目，讨论。

**选型**：

- Go 可能是 Java 的更好继承者，适合构建大型分布式系统Kubernetes 和 Docker
- Rust更适用于对时间/空间要求苛刻的场景。微控制器，Web Assembly。Rust 更类似于C++





#### 1.2.2 rust与c的对比

相同：

- Rust 和 C 都是直接对硬件的抽象，看做可移植汇编程序 
- Rust 和 C 都能控制数据结构的内存布局、整数大小、栈与堆内存分配、指针间接寻址等，并且⼀般都能翻译成可理解的机器代码，编译器很少插⼊ "魔法" 
- 基于返回值的错误处理

差异（rust的改进，开销）：

- Rust有更高层结构，迭代器、特质（trait）  和智能指针（现代c++也有）
  - 被设计为可预测地优化为简单的机器代码（又称 "零成本抽象"）  
- Rust的类型的内存布局更简单，直接
  - 控制对象复制、拷贝，值传递与引用
- Rust缺乏隐式类型转换和只用usize的索引（适合64位平台，空间开销大一点，但是容易对齐）
- Rust 中的字符串，会携带指针和长度。
- Rust的标准库中 I/O 是不带缓存的，需要使用BufWriter来包装，否则IO性能极差
- Rust可执行文件件会捆绑自己的标准库（300KB或更多）  ，不用操作系统内置的标准c库

rust明显优势：

- 编译检查，消除数据竞争，天生线程安全，解放多线程生产力；编译期计算，类似C++，常量求值
  - 所有权机制，Rust 语言借助类型系统，承载其“内存安全”的思想，表达出来的安全编程语义和模型。
    - 每个被分配的内存都有一个独占其所有权的指针。只有当该指针被销毁时，其对应的内存才能随之被释放。
  - 借用和生命周期。
    - 每个变量都有其生命周期，一旦超出生命周期，变量就会被自动释放。如果是借用，则可以通过标记生命周期参数供编译器检查的方式，防止出现悬垂指针，也就是释放后使用的情况。
  - 生态库，数据并行、线程池、队列、任务、无锁数据结构等
- 支持异步高并发编程
  - `async/await`异步编程模型
    - `Future` 表示一个尚未得出的值，你可以在它被解决以得出那个值之前对它进行各种操作。
      - 可以是异步io结果（返回可能值，超时）
      - 可以是不属于 I/O 的工作或者需要放到某个线程池中运行的CPU密集型的工作
      - 大多数语言实现基于回调方法，代价是需要写很多分配性的代码以及使用动态派发，性能开销，以及必须执行
    - Rust使用执行器（executor）的组件去轮询 `Future`，而非`Future` 来调度回调函数
      - 可取消执行
      - 无动态派发，满足零成本原则
    - Rust使用执行器（executor）调度，反应器（reactor）处理所有的 I/O，用户实际代码，组件边界整洁。

rust明显缺点:

- **编译速度很慢**，**增量编译功能不强**





## 1.3 生态、应用

#### 1.3.1 应用

作为高级系统级编程语言，其应用领域基本可以同时覆盖 C/CPP/Java/Go/Python 的应用领域。

官方主推的几个领域。

- WebAssembly
- 网络
- 嵌入式



##### 数据服务

数据库，数据仓库，数据流，大数据，分布式系统等

例子：

[TiKV](https://github.com/tikv/tikv)(分布式数据库)，[TensorBase](https://github.com/tensorbase/tensorbase)(实时数仓)，[Dataflow](https://github.com/TimelyDataflow/timely-dataflow)(实时数据流)，[Vector](https://github.com/timberio/vector)(数据管道)

[**Apache Arrow-rs**](https://github.com/apache/arrow-rs) (大数据/数据格式标准)

[InfluxDB IOx](https://github.com/influxdata/influxdb_iox) （国外/ 开源/时序数据库）

CeresDB （国内/商业/时序数据库）蚂蚁

[tantivy](https://github.com/tantivy-search/tantivy) (国外/开源/全文检索,lucene)

[Rucene](https://github.com/zhihu/rucene) （国内/开源/搜索引擎） 知乎



##### 云原生

云原生领域包括：机密计算、Serverless、分布式计算平台、容器、WebAssembly、运维工具等

例子：

[StratoVirt](https://gitee.com/openeuler/stratovirt) （国内/开源/容器，虚拟化平台）华为OpenEuler

[Firecracker](https://github.com/firecracker-microvm/firecracker) （国外/开源/产品）AWS，基于KVM的轻量级的microVM， 可以同时支持多租户容器和FaaS场景

[Krustlet](https://deislabs.io/posts/introducing-krustlet/) （国外/产品，Kubernetes/ WebAssembly/ 容器）微软，rust版k8s



##### 操作系统

使用 Rust 实现的各种操作系统

[Rust for Linux](https://github.com/Rust-for-Linux/linux) （国外/ Rust 进入 Linux 支持项目 ）推动 Rust 成为 Linux 内核第二编程语言

[Occulum](https://github.com/occlum/occlum) （国内/开源/TEE 库操作系统，机密计算/ 可信计算/ TEE / 库操作系统） 蚂蚁

[Redox](https://gitlab.redox-os.org/redox-os/redox/) （国外/ 开源/ 操作系统） 已经134w行



##### 机器学习

基于 Rust 实现的机器学习框架、科学计算库等等

[linfa](https://github.com/rust-ml/linfa) （国外/开源/机器学习工具包）

[tokenizers](https://github.com/huggingface/tokenizers) (国外/开源/自然语言处理分词库)

[ndarray](https://github.com/rust-ndarray/ndarray) （国外/开源/科学计算） rust 官方团队成员



##### 游戏

使用 Rust 制作的游戏、Rust 游戏引擎、Rust 游戏生态建设等

[veloren](https://github.com/veloren/veloren) (国外/沙盒游戏/开源)

[A/B Street](https://github.com/a-b-street/abstreet) (国外/开源/街景交通探索游戏) 城市规划

[rust-ecosystem](https://github.com/EmbarkStudios/rust-ecosystem) Embark 公司 与 Rust 游戏生态库



国内公司：

华为，PingCAP，阿里云/ 钉钉，蚂蚁集团机密计算和数据库

字节跳动/飞书(跨平台客户端组件)

知乎(搜索引擎)

收钱吧(消息队列)

吉利(区块链)

上海息未信息科技，航天及航空训练装备的研发生产

杭州秘猿(区块链)



#### 1.3.2 生态基础库和工具链

> Rust 生态日趋丰富，很多基础库和框架都会以 包（crate） 的方式发布到 [crates.io](https://crates.io/crates)。
>
> 截止目前，按包的使用场景分类，[http://Crates.io](http://crates.io/) 最流行的几个场景依次如下：
>
> - 命令行工具 （3133 crates）
> - no-std 库 （2778 crates）
> - 开发工具（测试/ debug/linting/性能检测等， 2652 crates）
> - Web 编程 （1776 crates）
> - API 绑定 （方便 Rust 使用的特定 api 包装，比如 http api、ffi 相关api等，1738 crates）
> - 网络编程 （1615 crates）
> - 数据结构 （1572 crates）
> - 嵌入式开发 （1508 crates）
> - 加密技术（1498 crates）
> - 异步开发（1487 crates）
> - 算法 （1200 crates）
> - 科学计算（包括物理、生物、化学、地理、机器学习等，1100 crates）



### REF

- [Rust官网](https://www.rust-lang.org/zh-CN/)
- [新项目用 Rust 还是 Go ？](https://zhuanlan.zhihu.com/p/134009415)
- [Swift程序员对Rust印象：内存管理](https://zhuanlan.zhihu.com/p/112898627)
- [一位 Rust 开发者的 Go 初体验](https://zhuanlan.zhihu.com/p/111305276) rust 核心开发者
- [我们是如何设计 Rust & 分布式存储教程的？ | Talent Plan 背后的故事](https://zhuanlan.zhihu.com/p/73950816)
- [哪些软件应用值得用Rust重写？](https://www.zhihu.com/question/305486448)
- [RustCon Asia 实录 | Rust 在国内某视频网站的应用](https://zhuanlan.zhihu.com/p/67941332) 
- [三万言｜2021 年 Rust 行业调研报告](https://zhuanlan.zhihu.com/p/383034421) （rust语言特点+行业应用）推荐



## 2. 语言学习

### 2.1 helloworld

`cargo new hello-rust` 通过`cargo new`命令创建一个基础rust项目：

```
hello-rust
|- Cargo.toml
|- src
  |- main.rs
```

- `Cargo.toml` 为 Rust 的清单文件。其中包含了项目的元数据和依赖库。
- `src/main.rs` 为编写应用代码的地方。

```
fn main() {
    println!("Hello, world!");
}
```

**运行（先会编译,即build）**：`cargo run`

实际编译完成后，可以直接执行`./target/debug/hello-rust`

`cargo`  是 Rust 的构建系统和包管理器。

添加依赖和使用，`Cargo.toml` 文件（[TOML](https://toml.io/cn/v1.0.0)是一种配置文件格式）：

```
[dependencies]
ferris-says = "0.2"
```

**安装依赖**：`cargo build`

产生`Cargo.lock`，该文件记录了本地所用依赖库的精确版本。

使用依赖的箱子crate（类似c/c++ use 库）

```rust
use ferris_says::say;
```

项目需要发布时，`cargo build --release` 优化编译项目，可以运行的更快，但是编译时间更长。

#### 注释

文档注释

- `/// 为接下来的项生成帮助文档。`用来描述的它后面接着的项  。
- `//! 为注释所属于的项（译注：如 crate、模块或函数）生成帮助文档。`用来描述包含它的项， 一般用在模块文件的头部  

生成Html文档

`rustdoc main.rs` 

或者`cargo doc  `

#### 格式化输出

[`std::fmt`](https://doc.rust-lang.org/std/fmt/) 里面所定义的一系列[`宏`](https://rustwiki.org/zh-CN/rust-by-example/macros.html)来处理

- `print!`：将文本输出到控制台（io::stdout）。
- `println!`: 与 `print!` 类似，但输出结果追加一个换行符。
- `eprint!`：将文本输出到标准错误（io::stderr）。
- `eprintln!`：与 `eprint!` 类似，但输出结果追加一个换行符。
- `format!` ： 将格式化文本写到（输出到）字符串 （String）  

```rust
// 占位符号{}
println!("{} days", 31);
println!("{0}, this is {1}. {1}, this is {0}", "Alice", "Bob");

// 格式化，可以在 `:` 后面指定特殊的格式。
println!("{} of {:b} people know binary, the other half don't", 1, 2);

format!("{}", foo) -> "3735928559"
format!("0x{:X}", foo) -> "0xDEADBEEF"
format!("0o{:o}", foo) -> "0o33653337357"
```

- `fmt::Debug` ： 使用 `{:?}` 标记。 格式化文本以供调试使用。  
  - `#[derive(Debug)]  ` 属性允许，自动推导出自定义类型fmt::Debug实现
  - `{:#?}` 可以美化输出（层次化打印）
- `fmt::Display` ： 使用 {} 标记。 以更优雅和友好的风格来格式化文本。  
  - 自定义类型需要手动实现

### 2.2 基础语法

#### 2.2.1 变量绑定：let

```rust
// 1) 不可变绑定, 类似于常量声明
let a1 = 5;  // 默认i32
let a2:i32 = 5;

// 2) 可变绑定，类似于变量，可以改变值，但是不允许改变类型
// 变量a， 可以改变绑定到变量的值
let mut a: f64 = 1.0;
//改变 a 的绑定
a = 2.0;
println!("{:?}", a);
//重新绑定为不可变，导致a不可变。掩蔽shadow，实际这样还可以让a绑定到不同的类型上。
//注意：具有作用域概念，离开作用域后被shadow变量，会匹配原来的模式。
let a = a;

// 3) let实际上是一种模式匹配
// let <pattern>: <type> = <expression>;并且: <type>和= <expression>都是可选的。
// let本身并无法控制声明的变量的可变性，实际由模式决定。
let (a, mut b): (bool,bool) = (true, false);
println!("a = {:?}, b = {:?}", a, b);

struct Point(f32, f32);
fn pick_a_point() -> Point;
//可以调用该函数并将整个 Point 存储到一个变量中并使用它
let new_point = pick_a_point();
println!("Picked the point at ({}, {})", new_point.0, new_point.1);

//给出一个模式，将结构拉开并将其各个位存储在单独的变量中
let Point(new_x, new_y) = pick_a_point();
println!("Picked the point at ({}, {})", new_x, new_y);
```



**常量**：

- `const`：不可改变的值（通常使用这种）。
- `static`：具有 [`'static`](https://rustwiki.org/zh-CN/rust-by-example/scope/lifetime/static_lifetime.html) 生命周期的，可以是可变的变量（使用 `static mut` ）。

```rust
const  THRESHOLD: i32 = 10;
// 全局变量
static LANGUAGE: &'static str = "Rust";
```



#### 2.2.2 原生类型Primitive Types

- 布尔类型：有两个值`true`和`false`。
- 字符类型：表示单个Unicode字符，存储为**4个字节**。
- 数值类型：
  - 有符号整数 (`i8`, `i16`, `i32`, `i64`, `isize`)
    - size：自适应操作系统的位数，64位系统即是64，但是与i64比较或者赋值时需要强制转换
  -  无符号整数 (`u8`, `u16`, `u32`, `u64`, `usize`) 
  - 浮点数 (`f32`, `f64`)。
    - 默认f64
- **数组**：具有固定大小，并且元素都是同种类型，可表示为`[T; N]`。
  - T表示类型，N表示长度
  - N需要是在编译时，就已知的整形值
  - N是类型的一部分，[u8;3] != [u8;4]
  - 下标从0开始
- **切片**：引用一个数组的部分（或全部）数据并且不需要拷贝，可表示为`&[T]`。
  - 可以作为函数的数组类型参数传递，接受不同长度的数组
  - &[..] 表示引用全部数组
  - 遵循左闭右开原则
  - 下标从0开始
- **元组**：具有固定大小的有序列表，每个元素都有自己的类型，通过解构或者索引来获得每个元素的值。`(T1, T2, ...) `
  - 元组可以充当函数的参数和返回值  
- **指针**：最底层的是裸指针`*const T`和`*mut T`，但解引用它们是不安全的，必须放到`unsafe`块里。
  - 解引用方式使用`*`
- **函数**：具有函数类型的变量实质上是一个函数指针。
  - 使用 `fn` 关键字来声明
  - 参数需要标注类型，`paramName: paramType`
  - `->` 之后指定返回值的类型，无返回值，则实际返回`()`，并且可省略`-> ()`
- 单元类型：即`()`，其唯一的值也是`()`这个空元组。

```rust
// boolean type
let t = true;
let f: bool = false;

// char type
let c = 'c';

// numeric types
let x = 42;
let y: u32 = 123_456;
let z: f64 = 1.23e+2;

// arrays and slices
let a = [0, 1, 2, 3, 4]; //定长数组
let middle = &a[1..4];  //切片，指向数组的一部分,[1, 2, 3]
let slice_right = &a[1..]; // 获得的元素为[1, 2, 3, 4]
let slice_left = &a[..3]; // 获得的元素为[0, 1, 2]

let mut ten_zeros: [i64; 10] = [0; 10]; // 所有元素可以初始化成相同的值,0

println!("first element of the array: {}", a[0]);  // 通过下标访问
println!("array size: {}", a.len()); //获取数组长度


// Tuple types
let tuple: (i32, &str) = (50, "hello");
let (fifty, _) = tuple;

// 包含各种不同类型的元组
// 创建单元素元组需要一个额外的逗号，这是为了和被括号包含的字面量作区分
let long_tuple = (1u8, 2u16, 3u32, 4u64,
    -1i8, -2i16, -3i32, -4i64,
    0.1f32, 0.2f64,
    'a', true);

// 通过元组的下标来访问具体的值
println!("long tuple first value: {}", long_tuple.0);
println!("long tuple second value: {}", long_tuple.1);

// 元组充当元组的元素
let tuple_of_tuples = ((1u8, 2u16, 2u32), (4u64, -1i8), -2i16);

// 元组打印
println!("tuple of tuples: {:?}", tuple_of_tuples);


// raw pointers
let x = 5;
let raw = &x as *const i32;
let points_at = unsafe { *raw };

// functions
fn foo(x: i32) -> i32 { x }
let bar: fn(i32) -> i32 = foo;
```

- 数值类型可以使用`_`分隔符来增加可读性。
- 一般使用使用`&`符号将`String`类型转换成`&str`类型，开销小，`to_string()`涉及内存分配
- 数组的长度是不可变的，动态的数组称为Vec (vector)，可以使用宏`vec!`创建。
  - 基于堆内存申请的连续动态数据类型

- 元组可以使用`==`和`!=`运算符来判断是否相同
- Rust不提供原生类型之间的隐式转换，只能使用`as`关键字显式转换。



##### 类型转换

- From的trait
  - 怎么根据另一种类型生成自己
  - 对于可能出错的转换，可以使用`TryFrom`，返回Result类型。
- Into
  - 与From相反，实现From，那么自动实现Into

```rust
// 标准库中实现的原生类型From
let my_str = "hello";
let my_string = String::from(my_str);

// 自定义
use std::convert::From;

#[derive(Debug)]
struct Number {
    value: i32,
}
// 实现 i32 生成Number类型
impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}

let num = Number::from(30);
// 必须指定into的类型
let num: Number = int.into();
```

- TryFrom/TryInto

  - 可能出错的转换，返回 [`Result`](https://doc.rust-lang.org/std/result/enum.Result.html) 型

- ToString/FromStr

  - ToString将其他类型转换为String，但是一般建议实现fmt::Display trait

  - FromStr将字符串转为目标类型

    `let parsed: i32 = "5".parse().unwrap();`

    `let turbo_parsed = "10".parse::<i32>().unwrap();`

#### 2.2.3 结构体与枚举

**结构体**（struct）有 3 种类型，使用 `struct` 关键字来创建：

- 元组结构体（tuple struct），事实上就是有名字的元组，使用也与元组类似。
- 经典的 [C 语言风格结构体](https://en.wikipedia.org/wiki/Struct_(C_programming_language))（C struct）。
  - 可嵌套定义
- 单元结构体（unit struct），不带字段，在泛型中很有用。

读：通过`.` 获取结构体的特定成员的值

写：要求整个结构体实例是可变的，然后进行赋值

```rust
// 单元结构体
struct Nil;

// 元组结构体
struct Pair(i32, f32);

// 带有两个字段（field）的结构体
struct Point {
    x: f32,
    y: f32,
}

struct Rectangle {
    p1: Point,
    p2: Point,
}

// 使用简单的写法初始化字段，并创建结构体
let name = "Peter";
let age = 27;
let peter = Person { name, age };
// 实例化结构体 `Point`
let point: Point = Point { x: 0.3, y: 0.4 };

// 访问 point 的字段
println!("point coordinates: ({}, {})", point.x, point.y);

// 使用结构体更新语法创建新的 point，这样可以用到之前的 point 的字段的值
let new_point = Point { x: 0.1, ..point };

// 使用 `let` 绑定来解构 point
let Point { x: my_x, y: my_y } = point;

let _rectangle = Rectangle {
    // 结构体的实例化也是一个表达式
    p1: Point { x: my_y, y: my_x },
    p2: point,
};

// 实例化一个单元结构体
let _nil = Nil;

// 实例化一个元组结构体
let pair = Pair(1, 0.1);

// 访问元组结构体的字段
println!("pair contains {:?} and {:?}", pair.0, pair.1);
```

**枚举**

`enum` 关键字允许创建一个从数个不同取值中选其一的枚举类型。

```rust
// 创建一个 `enum`（枚举）来对 web 事件分类。注意变量名和类型共同指定了 `enum`
// 取值的种类：`PageLoad` 不等于 `PageUnload`，`KeyPress(char)` 不等于
// `Paste(String)`。各个取值不同，互相独立。
enum WebEvent {
    // 一个 `enum` 可以是单元结构体（称为 `unit-like` 或 `unit`），
    PageLoad,
    PageUnload,
    // 或者一个元组结构体，
    KeyPress(char),
    Paste(String),
    // 或者一个普通的结构体。
    Click { x: i64, y: i64 }
}

let pressed = WebEvent::KeyPress('x');
// `to_owned()` 从一个字符串切片中创建一个具有所有权的 `String`。
let pasted  = WebEvent::Paste("my text".to_owned());
let click   = WebEvent::Click { x: 20, y: 80 };
let load    = WebEvent::PageLoad;
let unload  = WebEvent::PageUnload;


match event {
    WebEvent::PageLoad => println!("page loaded"),
    WebEvent::PageUnload => println!("page unloaded"),
    // 从 `enum` 里解构出 `c`。
    WebEvent::KeyPress(c) => println!("pressed '{}'.", c),
    WebEvent::Paste(s) => println!("pasted \"{}\".", s),
    // 把 `Click` 解构给 `x` and `y`。
    WebEvent::Click { x, y } => {
        println!("clicked at x={}, y={}.", x, y);
    },
}

```



### 2.3 面向对象

#### 2.2.1 方法

- 方法（method）是依附于对象的函数。
- 通过关键字 `self` 来访问对象中的数据和其他方法
  - `Self` 大写的S表示当前实现此tarit的类型
    - 在`Clone`的tarit中，返回Self类型的对象，其他方法有时需要返回`& Self`。
  - 方法参数中 `self`  等价于`self: Self`，`&self`参数等价于`self: &Self`,`&mut self`参数等价于`self: &mut Self`
    - `&mut self` 转成 `& Self`  使用 `&*self` 返回自身对象的引用
- 在impl代码块中定义

```rust
struct Point {
    x: f64,
    y: f64,
}

// 实现的代码块，`Point` 的所有方法都在这里给出
impl Point {
    // 这是一个静态方法（static method）
    // 静态方法不需要被实例调用
    // 这类方法一般用作构造器（constructor）
    fn origin() -> Point {
        Point { x: 0.0, y: 0.0 }
    }

    // 另外一个静态方法，需要两个参数：
    fn new(x: f64, y: f64) -> Point {
        Point { x: x, y: y }
    }   
}

pub struct AveragedCollection {
    list: Vec<i32>,
    average: f64,
}

impl AveragedCollection {
    // 实现公有方法
    pub fn add(&mut self, value: i32) {
        self.list.push(value);
        self.update_average();
    }

    pub fn remove(&mut self) -> Option<i32> {
        let result = self.list.pop();
        match result {
            Some(value) => {
                self.update_average();
                Some(value)
            },
            None => None,
        }
    }

    pub fn average(&self) -> f64 {
        self.average
    }

    // 私有方法
    fn update_average(&mut self) {
        let total: i32 = self.list.iter().sum();
        self.average = total as f64 / self.list.len() as f64;
    }
}
```



##### 闭包/lambda表达式

能够捕获周围作用域中变量的函数。

输入和返回类型两者都可以自动推导，而输入变量 名必须指明。

- 声明时使用 `||` 替代 `()` 将输入参数括起来
- 函数体定界符（`{}`）对于单个表达式是可选的，其他情况必须加上

```rust
let closure_annotated = |i: i32| -> i32 { i + 1 };
let closure_inferred  = |i     |          i + 1  ;
let i = 1;
println!("closure_annotated: {}", closure_annotated(i));
println!("closure_inferred: {}", closure_inferred(i));

let color = "green";
let print = || println!("`color`: {}", color);
print();

// 引用了可变变量，需要是可变闭包
let mut count = 0;
let mut inc = || {
    count += 1;
    println!("`count`: {}", count);
};
inc();
```

闭包作为输入参数

- Fn：
- FnMut
- FnOnce：闭包没有输入值和返回值

```rust
// 该函数将闭包作为参数并调用它。
fn apply<F>(f: F) where
    // 闭包没有输入值和返回值。
    F: FnOnce() {
    f();
}

// 输入闭包，返回一个 `i32` 整型的函数。
fn apply_to_3<F>(f: F) -> i32 where
    // 闭包处理一个 `i32` 整型并返回一个 `i32` 整型。
    F: Fn(i32) -> i32 {

    f(3)
}

// 闭包 `double` 满足 `apply_to_3` 的 trait 约束。
let double = |x| 2 * x;
println!("3 doubled: {}", apply_to_3(double));
```

##### 高阶函数

输入一个或多个 函数，并且/或者产生一个函数的函数。函数式编程风格。

```rust
let sum_of_squared_odd_numbers: u32 =
        (0..).map(|n| n * n)             // 所有自然数取平方
             .take_while(|&n| n < upper) // 取小于上限的
             .filter(|&n| is_odd(n))     // 取奇数
             .fold(0, |sum, i| sum + i); // 最后加起来
```





#### 2.3.2 特性trait

描述类型可以实现的抽象接口 (abstract interface)

- trait中可以定义默认方法
- trait中的方法可以被覆盖，重写override
- trait之间可以继承

```rust
trait HasArea {
    fn area(&self) -> f64;
}
struct Circle {
    x: f64,
    y: f64,
    radius: f64,
}
// Circle实现接口HasArea
impl HasArea for Circle {
    fn HasArea(&self) -> f64 {
        std::f64::consts::PI * (self.radius * self.radius)
    }
}
struct Square {
    x: f64,
    y: f64,
    side: f64,
}
// Square实现接口HasArea
impl HasArea for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }
}

trait Foo {
    fn foo(&self);
    // default method
    fn bar(&self) { println!("We called bar."); }
}
// inheritance
trait FooBar : Foo {
    fn foobar(&self);
}

struct Baz;
impl Foo for Baz {
    fn foo(&self) { println!("foo"); }
}
impl FooBar for Baz {
    fn foobar(&self) { println!("foobar"); }
}
```

##### 派生

通过 `#[derive]` 属性，编译器能够提供某些 trait 的基本实现。

另外可以被手动重写覆盖。

- 比较 trait: [`Eq`](https://doc.rust-lang.org/std/cmp/trait.Eq.html), [`PartialEq`](https://doc.rust-lang.org/std/cmp/trait.PartialEq.html), [`Ord`](https://doc.rust-lang.org/std/cmp/trait.Ord.html), [`PartialOrd`](https://doc.rust-lang.org/std/cmp/trait.PartialOrd.html)
- [`Clone`](https://doc.rust-lang.org/std/clone/trait.Clone.html), 用来从 `&T` 创建副本 `T`。
- [`Copy`](https://doc.rust-lang.org/core/marker/trait.Copy.html)，使类型具有 “复制语义”（copy semantics）而非 “移动语义”（move semantics）。
- [`Hash`](https://doc.rust-lang.org/std/hash/trait.Hash.html)，从 `&T` 计算哈希值（hash）。
- [`Default`](https://doc.rust-lang.org/std/default/trait.Default.html), 创建数据类型的一个空实例。
- [`Debug`](https://doc.rust-lang.org/std/fmt/trait.Debug.html)，使用 `{:?}` formatter 来格式化一个值。

```rust
// `Centimeters`，可以比较的元组结构体
#[derive(PartialEq, PartialOrd)]
struct Centimeters(f64);
```

##### Dyn 返回执行堆内存的trait的指针

Rust编译器需要知道每个函数的返回类型需要多少空间，那么每个函数必须返回具体的类型，对于派生对象，无法作为父类的类型的返回值，因为需要的内存空间大小不同。

所以，rust不直接返回一个trait对象，而是使用关键字`dyn`返回指向trait对象的指针。

```rust
struct Sheep {}
struct Cow {}

trait Animal {
    fn noise(&self) -> &'static str;
}
// 实现 `Sheep` 的 `Animal` trait。
impl Animal for Sheep {
    fn noise(&self) -> &'static str {
        "baaaaah!"
    }
}
// 实现 `Cow` 的 `Animal` trait。
impl Animal for Cow {
    fn noise(&self) -> &'static str {
        "moooooo!"
    }
}

// 返回一些实现 Animal 的结构体，但是在编译时我们不知道哪个结构体。
fn random_animal(random_number: f64) -> Box<dyn Animal> {
    if random_number < 0.5 {
        Box::new(Sheep {})
    } else {
        Box::new(Cow {})
    }
}

fn main() {
    let random_number = 0.234;
    let animal = random_animal(random_number);
    println!("You've randomly chosen an animal, and it says {}", animal.noise());
}
```



#### 2.3.3 泛型

泛型 (generics) ，也叫参数多态。

使用`<T>`部分表明它是一个泛型数据类型。

- 枚举
- 结构体
- 函数参数

```rust
// 枚举
enum Option<T> {
    Some(T),
    None,
}
let x: Option<i32> = Some(5);
let y: Option<f64> = Some(5.0f64);

// 结构体
// generic structs
struct Point<T> {
    x: T,
    y: T,
}
let int_origin = Point { x: 0, y: 0 };
let float_origin = Point { x: 0.0, y: 0.0 };

//函数
// generic functions
fn make_pair<T, U>(a: T, b: U) -> (T, U) {
    (a, b)
}
let couple = make_pair("man", "female");

// tarit一般使用关联类型
// use associated types
trait Graph {
    type N;
    type E;

    fn has_edge(&self, &Self::N, &Self::N) -> bool;
    fn edges(&self, &Self::N) -> Vec<Self::E>;
}
```

##### 约束

对泛型T类型，常常要求必须实现某种trait作为约束。

- 限制泛型类型为符合约束的类型
- 泛型的实例可以访问作为约束的 trait 的方法

```rust
// 定义一个函数 `printer`，接受一个类型为泛型 `T` 的参数，
// 其中 `T` 必须实现 `Display` trait。
fn printer<T: Display>(t: T) {
    println!("{}", t);
}
```

**多重约束**

 `+` 连接

```rust
fn compare_prints<T: Debug + Display>(t: &T) {
    println!("Debug: `{:?}`", t);
    println!("Display: `{}`", t);
}
```

**where分句**

- 分别指定泛型的类型和约束
- 

```rust
// 使用 `where` 从句来表达约束
impl <A, D> MyTrait<A, D> for YourType where
    A: TraitB + TraitC,
    D: TraitE + TraitF {}
```



#### 2.3.4 宏

使用 macro_rules! 来创建宏。

- 减少因为类型不同，而产生的重复代码。DRY（不写重复代码）
- 领域专用语言（DSL，domain-specific language），为特定的目的创造特定的语法
- 可变接口（variadic interface），接受不定数目参数的接口

```rust
macro_rules! say_hello {
    // `()` 表示此宏不接受任何参数。
    () => (
        // 此宏将会展开成这个代码块里面的内容。
        println!("Hello!");
    )
}
fn main() {
    // 这个调用将会展开成 `println!("Hello!");`,事实上println!也是一个宏，可以再展开。
    say_hello!()
}

#[macro_export]
macro_rules! with_timer_print {
    ($timer_name:ident, $($s:stmt);+ $(;)?) => {
        let $timer_name = ::std::time::Instant::now();
        $($s)*
        println!("{:?}", $timer_name.elapsed());
    };
}
```

语法：

- 指示符
  - 宏的参数使用一个美元符号 $ 作为前缀， 并使用一个指示符（designator）来 注明类型  
    - `ident` 指示符用于变量名或函数名
    - `expr` 指示符表示表达式
    - `pat` (**模式** *pattern*)
    - `stmt` (**语句** *statement*)
      - 代码块
    - `ty` (**类型** *type*)
- 重载
  - 宏可以重载，从而接受不同的参数组合。类似于匹配（match）代码块
- 重复
  - 宏事务参数列表 `+` 来表示一个参数可能出现一次或多次
  -  `*` 来表示该 参数可能出现零次或多次

```rust
macro_rules! create_function {
    // 此宏接受一个 `ident` 指示符表示的参数，并创建一个名为 `$func_name` 的函数。
    // `ident` 指示符用于变量名或函数名
    ($func_name:ident) => (
        fn $func_name() {
            // `stringify!` 宏把 `ident` 转换成字符串。
            println!("You called {:?}()",
                     stringify!($func_name))
        }
    )
}
// 借助上述宏来创建名为 `foo` 和 `bar` 的函数。
create_function!(foo);

/// 2.重载
// 根据你调用它的方式，`test!` 将以不同的方式来比较 `$left` 和 `$right`。
macro_rules! test {
    // 参数不需要使用逗号隔开。
    // 参数可以任意组合！
    ($left:expr; and $right:expr) => (
        println!("{:?} and {:?} is {:?}",
                 stringify!($left),
                 stringify!($right),
                 $left && $right)
    );
    // ^ 每个分支都必须以分号结束。
    ($left:expr; or $right:expr) => (
        println!("{:?} or {:?} is {:?}",
                 stringify!($left),
                 stringify!($right),
                 $left || $right)
    );
}

test!(1i32 + 1 == 2i32; and 2i32 * 2 == 4i32);
test!(true; or false);


// 3. 重复
// `min!` 将求出任意数量的参数的最小值。
macro_rules! find_min {
    // 基本情形：
    ($x:expr) => ($x);
    // `$x` 后面跟着至少一个 `$y,`
    ($x:expr, $($y:expr),+) => (
        // 对 `$x` 后面的 `$y` 们调用 `find_min!` 
        std::cmp::min($x, find_min!($($y),+))
    )
}
```



#### 2.3.5 模块和包系统

##### 包crate

`crate` 是一个**独立的可编译单元**。

编译后，会对应着生成一个可执行文件或一个库。

每个包，都有一个入口文件（main.rs，lib.rs）。

##### 模块module

关键字 `mod`，可以在一个文件中定义一个模块，或者引用另外一个文件中的模块。

目的：

- 分隔逻辑块
- 提供适当的函数，或对象，供外部访问

特点：

1. 每个 crate 中，默认实现了一个隐式的 `根模块（root module）`；
2. 模块的命名风格也是 `lower_snake_case`，跟其它的 Rust 的标识符一样；
3. 模块可以嵌套；
4. 模块中可以写任何合法的 Rust 代码；

```rust
mod aaa {
    const X: i32 = 10;

    fn print_aaa() {
        println!("{}", 42);
    }

    mod bbb {
        fn print_bbb() {
            println!("{}", 37);
        }
    }
}

mod ccc {
    fn print_ccc() {
        println!("{}", 25);
    }

}
```

**可见性**

- 模块中的内容，默认是私有的，只有模块内部能访问。
-  `pub` 关键字可以暴露
  - 外部引用的时候，使用 `use` 关键字

```rust
//// 文件ccc.rs
mod ccc {
    pub fn print_ccc() {
        println!("{}", 25);
    }
}

/// 文件main.rs
mod  ccc;

fn main() {
    use ccc::print_ccc;

    print_ccc();
    // 或者
    ccc::print_ccc();
}
```

Rust的模块层级关系与实际文件系统的层级关系解耦。

- 优先查找xxx.rs 文件
  - main.rs、lib.rs、mod.rs中的mod xxx; 默认优先查找同级目录下的 xxx.rs 文件；
  - 其他文件yyy.rs中的mod xxx;默认优先查找同级目录的yyy目录下的 xxx.rs 文件；
- 如果 xxx.rs 不存在，则查找 xxx/mod.rs 文件，即 xxx 目录下的 mod.rs 文件。



**路径**

模块路径（self，super）,对模块的引用如`use a::b::c::d`

- `use self::xxx` 表示，加载当前模块中的 xxx。此时 self 可省略；
- `use xxx::{self, yyy}`，表示，加载当前路径下模块 xxx 本身，以及模块 xxx 下的 yyy；
- `super` 表示，当前模块路径的上一级路径，



##### PreLude

默认导入的内容。（类似java.lang）



### 2.4 常用工具箱、标准库

#### 2.4.1 字符串

字符串类型

- 字符串切片`&str`，有固定的大小，并且不可变
- 堆分配字符串`String`，可变。用于未知大小的文本。
  - 带有的 `vec:Vec<u8>` 成员的结构体

```rust
// string types
let str = "Hello, world!"; // &str 类型
// 附带显式类型标识
let hello: &'static str = "Hello, world!";

// 创建一个空的字符串
let mut s = String::new();
// 从 `&str` 类型转化成 `String` 类型
let mut hello = String::from("Hello, ");
// 压入字符和压入字符串切片
hello.push('w');
hello.push_str("orld!");

// 弹出
hello.pop();  //Some(Char)


// &str 连接
let con_str = ["xx1","xxx2"].join(" "); // "xx1 xx2"  String 类型
```



#### 2.4.2 集合类型

##### 动态数组Vec

数组长度不固定，可以在其尾部进行push或者pop操作（O(1)），使用堆空间。

```rust
// new声明
let mut v1: Vec<i32> = Vec::new();

// 宏声明
let v: Vec<i32> = vec![];
let v = vec![1, 2, 3];
let v = vec![0; 10]; //10个0的动态数组

//安全的，随机访问，避免直接通过下标访问，产生数组越界
assert_eq!(v.get(1), Some(&2));
assert_eq!(v.get(3), None);

// 遍历
for i in &v { .. } // 获得引用
for i in &mut v { .. } // 获得可变引用
```

##### 哈希表HashMap

HashMap要求一个可哈希（实现 Hash trait）可比较的Key类型，和一个编译时知道大小的Value类型。

可以通过编译期属性`#[derive(PartialEq, Eq, Hash)]`，派生。

```rust
use std::collections::HashMap;

// 声明
let mut come_from = HashMap::new();
// 插入
come_from.insert("WaySLOG", "HeBei");
come_from.insert("Mike", "HuoGuo");

// 查找key
if !come_from.contains_key("elton") {
    println!("Oh, 我们查到了{}个人，但是可怜的Elton猫还是无家可归", come_from.len());
}

// 根据key删除元素
come_from.remove("Mike");

// 利用get的返回判断元素是否存在
let who = ["MoGu", "Marisa"];
for person in &who {
    match come_from.get(person) {
        Some(location) => println!("{} 来自: {}", person, location),
        None => println!("{} 也无家可归啊.", person),
    }
}

// 遍历输出
for (name, location) in &come_from {
    println!("{}来自: {}", name, location);
}
```



#### 2.4.3 Option和unwarp

Option选项，用于处理“不存在”的可能的情况。

- `Some(T)`：找到一个属于 `T` 类型的元素
- `None`：找不到相应元素

选项可以通过 `match` 显式地处理，或使用 `unwrap` 隐式地处理，隐式处理要么 返回 `Some` 内部的元素，要么就 `panic`。

```rust
// match 显式处理
fn give_commoner(gift: Option<&str>) {
    // 指出每种情况下的做法。
    match gift {
        Some("snake") => println!("Yuck! I'm throwing that snake in a fire."),
        Some(inner)   => println!("{}? How nice.", inner),
        None          => println!("No gift? Oh well."),
    }
}
// unwrap 隐式处理
fn give_princess(gift: Option<&str>) {
    // `unwrap` 在接收到 `None` 时将返回 `panic`。
    let inside = gift.unwrap();
    if inside == "snake" { panic!("AAAaaaaa!!!!"); }

    println!("I love {}s!!!!!", inside);
}
```

使用`?` 解构`Option`:

如果 `x` 是 `Option`，则对于 `x?`，若 `x` 是 `Some` 则返回底层值，否则无论函数是否正在执行都将终止且返回 `None`。

```rust
fn next_birthday(current_age: Option<u8>) -> Option<String> {
    // 如果 `current_age` 是 `None`，这将返回 `None`。
    // 如果 `current_age` 是 `Some`，内部的 `u8` 将赋值给 `next_age`。
    let next_age: u8 = current_age?;
    Some(format!("Next year I will be {}", next_age))
}
```

`Option`的`map()` 方法，可用于传入的函数是 `Some -> Some` 和 `None -> None` 的，并且可以级联。

`and_then()` 使用被 `Option` 包裹的值来调用其输入函数并返回结果。 如果 `Option` 是 `None`，那么它返回 `None`。

还有另一个类似于 `unwrap` 的方法它还允许我们选择 `panic!` 的错误信息：`expect`，增加错误信息。

```rust
let f = File::open("hello.txt").expect("Failed to open hello.txt");
```



#### 2.4.4 结果Result

[`Result`](https://doc.rust-lang.org/std/result/enum.Result.html) 是 [`Option`](https://doc.rust-lang.org/std/option/enum.Option.html) 类型的更丰富的版本，描述的是可能的**错误**而不是可能的**不存在**。

Result用于处理可恢复的错误。

`Result<T，E>` 可以有两个结果的其中一个：

- `Ok<T>`：找到 `T` 元素
- `Err<E>`：找到 `E` 元素，`E` 即表示错误的类型。

同样可以用`?` 取出变量，但是不产生panic。

这里在TensorBase的源码分析中，发现作为Result经常作为函数的返回值类型。

同时，取代Java项目中经常出现throw Exception，直接return Err包装的错误信息。

这让的错误返回形式，比go，C++ 返回nil和 ret值，确实更优雅（Result可以同时表示正确结果或者错误信息）。

```rust
let f = File::open("hello.txt").unwrap_or_else(|error| {
    if error.kind() == ErrorKind::NotFound {
        File::create("hello.txt").unwrap_or_else(|error| {
            panic!("Problem creating the file: {:?}", error);
        })
    } else {
        panic!("Problem opening the file: {:?}", error);
    }
});
```





#### 2.4.5 控制流程语句

###### fo in

`for in` 结构可以遍历 Iterator。

创建迭代器的一个最简单的方法是使用区间标记`a..b` 生成[a,b)区间，步长为1。

`a..=b` 区间为[a,[:qa]]

```rust
for i in 0..100 {
    //xxxx
}
```



### 2.5 高级特性

#### 2.5.1 所有权系统

##### 所有权Ownership

- 绑定Binding
  - 将目标`资源`(内存，存放value)`绑定`到某个`标识符`。

```rust
let x: i32;       // 标识符x, 没有绑定任何资源
				  //一般不这样做，以免未初始化而使用，rust不会自动初始化任何变量
let y: i32 = 100; // 标识符y，绑定资源100
				  // y是资源100的所有者
```

- 移动move
  - 将所有权转移到另一个标识符。
  - 当所有权转移时，数据的可变性可能发生改变。
  - 所有权被移动后，原变量的内存立刻失效。

```rust
let a: String = String::from("xyz");
let b = a;  // a把资源的所有权绑定转移到b，然后a未绑定任何资源前，无法再使用，避免悬挂指针的产生。
//println!("{}", a);
// 同一时刻，rust的资源有且只有一个所有者，以保证释放资源时不会重复释放

// 但是可以掉用clone方法，创建新的资源
let a: String = String::from("xyz");
let b = a.clone();
println!("{}", a);
```

- 拷贝Copy
  - 实现Copy特性的变量类型，在move时，会拷贝资源到新的内存区域，并将新资源绑定到目标变量。

```rust
let a: i32 = 100;
let b = a; //发生拷贝，绑定到新资源
println!("{}", a); // a依然绑定在原资源上面
```

原生数据类型Primitive Types，均实现了Copy特性。还有的常用类型[Result](https://doc.rust-lang.org/std/result/enum.Result.html)<T, E>，[Options](https://doc.rust-lang.org/test/test/struct.Options.html) 

，完整说明见[Copy](https://doc.rust-lang.org/std/marker/trait.Copy.html)

- 可变性
  - 可变绑定，必须用关键字mut声明绑定为可变。
  - 不可变绑定与常量const完全不同，不可变绑定是用来**约束绑定行为**，**“不可变绑定”不能通过原“所有者”更改资源内容**。
  - 严格区分绑定的可变性，以便编译器可以更好的优化，也提高了内存安全性。

```rust
let mut a: i32 = 100;  // 通过关键字mut声明a是可变的
a = 200; // a绑定到资源200(的内存地址)

let a = vec![1, 2, 3];  //不可变绑定, a <=> 内存区域A(1,2,3)
let mut a = a;  //可变绑定， a <=> 内存区域A(1,2,3), 注意此a已非上句a，只是名字一样而已
a.push(4);
println!("{:?}", a);  //打印：[1, 2, 3, 4]， 内存区域A

let mut a: &str = "abc";  //可变绑定, a <=> 内存区域A("abc")
a = "xyz";    //绑定到另一内存区域, a <=> 内存区域B("xyz")
println!("{:?}", a);  //打印："xyz",内存区域B
```

##### 引用&借用References&Borrowing

- &引用，允许使用变量的值但不获取其所有权。
  - `ref` 和`ref mut` 也可以获取引用
- 按引用传递对象的方式称作借用(borrow)。

```rust
// let绑定的不可变变量x
let x: Vec<i32> = vec!(1i32, 2, 3);
// 借用，不会发生所有权move，所以可以通过x，y访问，同一份资源。
// 通过`&`引用变量x，let绑定到y，y是对变量x的不可变借用
let y = &x;
println!("x={:?}, y={:?}", x, y);


// 获得一个 `i32` 类型的引用。`&` 表示取引用。
let reference = &4;
match reference {
    // 如果用 `&val` 这个模式去匹配 `reference`，就相当于做这样的比较：
    // `&i32`（译注：即 `reference` 的类型）
    //    |
    // `&val`（译注：即用于匹配的模式）
    // ^ 我们看到，如果去掉匹配的 `&`，`i32` 应当赋给 `val`。
    // 译注：因此可用 `val` 表示被 `reference` 引用的值 4。
    &val => println!("Got a value via destructuring: {:?}", val),
}
// 如果不想用 `&`，需要在匹配前解引用。
match *reference {
    val => println!("Got a value via dereferencing: {:?}", val),
}

//`ref`。更改了赋值行为，从而可以对具体值创建引用
let ref _is_a_reference = 3;

// 变量
let value = 5;
let mut mut_value = 6;

match value {
    // 获取value的引用r
    ref r => println!("Got a reference to a value: {:?}", r),
}
// 类似地使用 `ref mut`。
match mut_value {
    // 获取对mut_value的可变引用m
    ref mut m => {
        // 已经获得了 `mut_value` 的引用，先要解引用，才能改变它的值。
        *m += 10;
        println!("We added 10. `mut_value`: {:?}", m);
    },
}
```

可变性：

- 不可变借用， `&T`
- 可变借用，`&mut T`，借用的变量本身必须有可变性

规则：

- 在任意给定时间，**要么** 只能有一个可变引用，**要么** 只能有多个不可变引用。
- 借用在离开作用域后释放。
- 在可变借用释放前不可访问源变量。
- 引用必须有效。引用失效前，目标必须存活且不可改变（来自所有者的改变）。即借用周期小于被借用者（所有者）的生命周期。

```rust
let x: Vec<i32> = vec!(1i32, 2, 3);

//可同时有多个不可变借用
let y = &x;
let z = &x;
let m = &x;

println!("{:?}, {:?}, {:?}, {:?}", x, y, z, m)

//源变量x可变性
let mut x: Vec<i32> = vec!(1i32, 2, 3);
{
//只能有一个可变借用
let y = &mut x;
// let z = &mut x; //错误
y.push(100);

//ok
println!("{:?}", y);

//错误，可变借用未释放，源变量不可访问，保证只有一个在读写
// println!("{:?}", x);
}
//可变借用已经释放，可以访问
println!("{:?}", x);
```



##### 生命周期

变量的从创建开始到被销毁的时间区间。生命周期的主要目标是避免悬垂引用。

- 隐式，大部分时候生命周期是隐含并可以推断的。
- 显式如`'a` a只是一个简写表示，用于在无法自动推导生命周期时，人为指定，那个变量的生命周期。以保证运行时的引用时有效的。
  - 比如结构体中使用到引用变量，需要显示标记其引用的生命周期

Rust的惯例，用`'a`,`'b`,`'c`这样的写法。

生命周期的推导

- 输出值（也称为返回值）依赖哪些输入值
- 输入值的Lifetime大于或等于输出值的Lifetime (准确来说：子集，而不是大于或等于)

```rust
// 'b: 'a, 显式的告诉编译期，生命周期'b比'a 长。
// 指定返回值的生命周期为'a
fn foo<'a, 'b: 'a>(x: &'a str, y: &'b str) -> &'a str {
    if true {
        x
    } else {
        y
    }
}
```

结构体中使用借用

```rust

struct Person<'a> {
    // 必须声明age借用的的生命周期，以确保Person的生命周期不会比age借用长，产生悬空指针。
    age: &'a u8, 
}

impl<'a> Person<'a> {
    fn print_age(&self) {
        println!("Person.age = {}", self.age);
    }
}

let x = 20_u8;
let stormgbs = Person {
    age: &x,
};
```



`'static`类型的Lifetime是整个程序的运行周期。

字符串"hello, world!"的类型是`&'static str`。

- 使用 `static` 声明来产生常量（constant）。
- 产生一个拥有 `&'static str` 类型的 `string` 字面量。



生命周期省略规则：

- 作为引用的每个函数或方法的输入参数都有自己的生命周期参数

  - `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`

- 只有一个输入生命周期参数，则该生命周期将分配给所有输出生命周期参数

  - `fn foo<'a>(x: &'a i32) -> &'a i32`

- 如果有多个输入生命周期参数，但其中一个是`&self`或`&mut self`(即方法)，则生命周期`self` 被分配给所有输出生命周期参数。

  - ```rust
    impl<'a> ImportantExcerpt<'a> {
    	// &str 实际为 &'a str
        fn announce_and_return_part(&self, announcement: &str) -> &str {
            println!("Attention please: {}", announcement);
            self.part
        }
    }
    ```

    

**堆栈区别**

- 栈
  - 栈中的所有数据都必须占用已知且固定的大小。后进先出。
  - 入栈比在堆上分配内存要快，操作系统无需为存储新数据去搜索内存空间
- 堆
  - 编译时大小未知或大小可能变化的数据。
  - 访问堆上的数据比访问栈上的数据慢，因为必须通过指针来访问。
  - Rust用所有权系统来管理堆上的数据



###### 借用实践例子

函数

```rust
// 函数中处理
fn take_the_n(n: &mut u8) {
    *n += 2;
}
fn take_the_s(s: &mut String) {
    s.push_str("ing");
}

let mut n = 5;
let mut s = String::from("Borrow");

take_the_n(&mut n);
take_the_s(&mut s);
```

match

 `match` 表达式中，默认情况下会对匹配臂中的值进行`move`，除非它是 `Copy` 类型。

```rust
#[derive(Debug)]
enum Food {
    Cake,
    Pizza,
    Salad
}
#[derive(Debug)]
struct Bag {
    food: Food
}

let bag = Bag { food: Food::Cake };
match bag.food {
    Food::Cake => println!("I got cake"),
    // 关键字ref可以通过引用来匹配元素，而不是根据值来获取它们
    ref a => println!("I got {:?}", a)
}
```



### 2.6 高性能库

#### 2.6.1 并发，并行，多线程编程

**使用 spawn 创建新线程**

`thread::spawn` 函数

```rust
use std::thread;
use std::time::Duration;
// 注意：当主线程结束时，新线程也会结束，而不管其是否执行完毕
let handle =  thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {} from the spawned thread!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

// 使用join等待所有线程结束，阻塞在这里，join的位置是有影响的！
handle.join().unwrap();
```

**move 闭包**

`thread::spawn` 支持从环境的线程（例如主线程）获取变量的借用，但是需要保证，变量的生命周期时安全。所以引入`move` 关键字强制闭包获取其使用的环境值的所有权。

```rust
let v = vec![1, 2, 3];
let handle = thread::spawn(move || {
println!("Here's a vector: {:?}", v);
});

// 此时无法再主线程中使用v
//  drop(v); // oh no!
handle.join().unwrap();
```

##### 线程间消息传递

“通过共享消息来共享内存”

**通道Channel**

- 发送者transmitter
- 接受者receiver
- 当发送者或接收者任一被丢弃时，通道被**关闭**（*closed*）

```rust
use std::sync::mpsc;
//创建一个通道，并将其两端赋值给 tx 和 rx
let (tx, rx) = mpsc::channel();
// mpsc 是多个生产者，单个消费者（multiple producer, single consumer）的缩写

//将tx移动到一个新建的线程中并发送 “hi”
thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
    	// send 函数获取其参数的所有权并移动这个值归接收者所有
    	// 接受者可能会修改或删除该值，所以无法使用该值
    	// println!("val is {}", val);
    });
//在主线程中接收并打印内容 “hi”
let received = rx.recv().unwrap();
println!("Got: {}", received);
```

`recv` 阻塞主线程执行直到从通道中接收一个值

`try_recv` 非阻塞，立即返回`Result<T, E>`（有结果ok，无结果Err），可以在主线程做其他事情，循环调用`try_recv`在消息到达后处理结果。

```rust
use std::thread;
use std::sync::mpsc;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];
		// 发送多个值
        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });
	// 将rx当作一个迭代器，打印输出
    // 当通道被关闭时，迭代器也将结束
    for received in rx {
        println!("Got: {}", received);
    }
}
```

使用克隆创建多生产者

```rust
let (tx, rx) = mpsc::channel();
// 增加生产者
let tx1 = tx.clone();

let tx1 = tx.clone();
thread::spawn(move || {
    let vals = vec![
        String::from("hi"),
        String::from("from"),
        String::from("the"),
        String::from("thread"),
    ];

    for val in vals {
        tx1.send(val).unwrap();
        thread::sleep(Duration::from_secs(1));
    }
});
thread::spawn(move || {
    let vals = vec![
        String::from("more"),
        String::from("messages"),
        String::from("for"),
        String::from("you"),
    ];

    for val in vals {
        tx.send(val).unwrap();
        thread::sleep(Duration::from_secs(1));
    }
});

for received in rx {
    println!("Got: {}", received);
}
```

##### 共享状态（变量）

**互斥器**（*mutex*），任意时刻，其只允许一个线程访问某些数据

- 在使用数据之前尝试获取锁
- 处理完被互斥器所保护的数据之后，释放锁

```rust
use std::sync::Mutex;
use std::thread;

// 创建互斥变量
// 智能指针 Arc<T>来创建引用计数的值，以便拥有多所有者
// 原子引用计数确保可以安全的在多个线程间共享
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    // 将所有权移入线程之前克隆Arc<T>
    // 克隆时增加计数，离开作用域，被丢弃时，减少计数。
    let counter = Arc::clone(&counter);
	let handle = thread::spawn(move || {
	// lock，阻塞方式尝试获取锁
    // 如果另一个线程拥有锁，并且那个线程panic了，则lock调用会失败，
    // 遇到这种情况使用unwrap发出panic
    // lock返回一个MutexGuard的智能指针,
    // 提供了一个Drop实现当MutexGuard离开作用域时自动释放锁
    // 锁的释放是自动发生的。
	let mut num = counter.lock().unwrap();
	*num += 1;
	});
	handles.push(handle);
}
// 等待所有线程执行结束
for handle in handles {
	handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());
```



#### 2.6.2 Send 和 Sync

Rust感知的并发概念Sync和Send trait。

##### Send允许线程间转移所有权

`Send` 标记 trait 表明类型的所有权可以在线程间传递。

- 几乎所有的 Rust 类型都是`Send` 的，例外的是如 `Rc<T>` 多所有者。

- 几乎所有基本类型都是 `Send` 的，除了裸指针（raw pointer）。

- 任何完全由 `Send` 的类型组成的类型也会自动被标记为 `Send`。



##### Sync允许多线程访问

`Sync` 标记 trait 表明一个实现了 `Sync` 的类型可以安全的在多个线程中拥有其值的引用。

即，对于任意类型 `T`，如果 `&T`（`T` 的引用）是 `Send` 的话 `T` 就是 `Sync` 的。

- 基本类型是 `Sync` 的，完全由 `Sync` 的类型组成的类型也是 `Sync` 的。

智能指针 `Rc<T>` 也不是 `Sync` 的。



#### 2.6.3 Unsafe、原始指针、智能指针

##### Unsafe

rust静态分析，是保守派，怀疑可能出问题。

unsafe Rust， 提供机制，告诉编译器，我确信没有问题，允许不安全操作。

通过 `unsafe` 关键字来切换到不安全 Rust，开启一个新的存放不安全代码的块

- 解引用原始指针（raw pointer）
- 调用不安全的函数或方法
- 访问或修改可变静态变量
- 实现不安全 trait
- 访问 `union` 的字段

`unsafe` 并不会关闭借用检查器或禁用任何其他 Rust 安全检查，只是提供了这五个不会被编译器检查内存安全的功能。



##### 原始指针

`*const T` 和`* mut T` 表示原始、不安全指针。是rust的一种原生类型。

- 使用原始指针，必须使用`unsafe`。
  - 创建，声明时不用
  - 也有一些安全的方法，可以不用safe包含起来，比如`is_null()`
- 原始指针可以是未对其unaligned 或 null的。但是解引用`*` 时，必须非null和对齐的。
- 原始指针不会获取变量的所有权。

```rust
let my_num: i32 = 10;
// 创建原始指针my_num_ptr，指向不可变变量my_num
let my_num_ptr: *const i32 = &my_num;

let mut my_speed: i32 = 88;
// 创建原始指针my_speed_ptr，指向可变变量my_speed
let my_speed_ptr: *mut i32 = &mut my_speed;

// 获取在堆上对象的指针
// 通过Box，my_num是放在堆上的变量
let my_num: Box<i32> = Box::new(10);
// 通过*解引用，然后再&获取地址
let my_num_ptr: *const i32 = &*my_num;
let mut my_speed: Box<i32> = Box::new(88);
let my_speed_ptr: *mut i32 = &mut *my_speed;

// 也可以通过into_raw方法获取原始指针
let my_speed: Box<i32> = Box::new(88);
let my_speed: *mut i32 = Box::into_raw(my_speed);

// 用libc 获取
extern crate libc;
use std::mem;
unsafe {
    let my_num: *mut i32 = libc::malloc(mem::size_of::<i32>()) as *mut i32;
    if my_num.is_null() {
        panic!("failed to allocate memory");
    }
    libc::free(my_num as *mut libc::c_void);
}

// 指针的常用方法
// offset()
let s: &str = "123";
let ptr: *const u8 = s.as_ptr();
unsafe {
    // 通过offset自动计算指针下一个对象地址
    println!("{}", *ptr.offset(1) as char);
    println!("{}", *ptr.offset(2) as char);
}

```



[primitive.pointer](https://doc.rust-lang.org/1.54.0/std/primitive.pointer.html)

##### 智能指针

**智能指针**（*smart pointers*）是一类数据结构，他们的表现类似指针，但是拥有额外的元数据和功能。

一个常用的类型是 **引用计数** （*reference counting*）智能指针类型，其允许数据有多个所有者，当没有任何所有者时负责清理数据（在 Rust 中，每当值离开作用域时，编译器会自动插入这些调用Drop的方法的代码完成资源释放，其他如C++需要手动调用析构函数）。

Rust普通引用和智能指针的区别：引用一般只是借用数据（可变借用，不可变借用）的指针，而智能指针是拥有指向的数据（有所有权，并且可以修改），带有元数据，和额外的功能与保证。

 `String` 和 `Vec<T>` 本质上就是智能指针。

```rust
pub struct String {
    vec: Vec<u8>,
}
pub struct Vec<T> {
    buf: RawVec<T>,
    len: usize,
}
```

智能指针通常使用结构体实现，其实现了 `Deref` 和 `Drop` trait，用于引用和清理数据。

-  实现`Deref` trait 用于使指针当做常规引用，通过解引用符号* 获取指向的对象

  - `*p` 时，实际为 `*(p.deref())` ，deref方法返回引用

  -  `Deref` 还被用于在函数和放啊传参是，进行隐式的强制类型转换，避免过多的使用&和*

    - 当这种特定类型的**引用**作为实参传递给和形参类型不同的函数或方法时，Deref 强制转换将自动发生。

      - 注意是实现 `Deref`的智能指针的引用

        ```rust
        fn hello(name: &str) {
            println!("Hello, {}!", name);
        }
        let m = MyBox::new(String::from("Rust"));
        // 指针m的引用
        // 过程：
        // 1.通过 deref调用将 &MyBox<String> 变为 &String (MyBox实现的Deref)
        // 2.通过 deref调用将&String 变为字符串slice &str (String实现的Deref)
        hello(&m);
        // 没有Deref，就需要这样写
        hello(&(*m)[..]);
        ```

  - `Deref`实现不可变解引用，`DerefMut`实现可变解引用

标准库中常用的智能指针：

- `Box<T>`，用于在堆上分配值
- `Rc<T>`，一个引用计数类型，其数据可以有多个所有者
  - `Arc<T>` 可线程间安全传递
- `Ref<T>` 和 `RefMut<T>`，通过 `RefCell<T>` 访问。（ `RefCell<T>` 是一个在运行时而不是在编译时执行借用规则的类型）。

###### Box\<T>

 box 允许将一个值放在堆上而不是栈上。留在栈上的则是指向堆数据的指针。数据被储存在堆上而不是栈上，box 没有性能损失。

Box 遵循 Rust 的所有权规则，在赋值时，数据和指针的所有权都被移动(move)。（等价于C++的 unique pointer唯一指针）

场景：

- 当有一个在编译时未知大小的类型，而又想要在需要确切大小的上下文中使用这个类型值的时候
  - 创建递归类型，值的一部分是相同类型的另一个值。
- 当有大量数据，并希望在确保数据不被拷贝的情况下转移所有权的时候，值需要拷贝栈上的指针
- 当希望拥有一个值并只关心它的类型是否实现了特定 trait，而不是其具体类型的时候
  - 与dyn关键字结合，完成面向对象设计的多态，见2.3.2

```rust
// 定义变量 b，其值是一个指向被分配在堆上的值5的Box
let b = Box::new(5);
println!("b = {}", b);


// 创建递归类型 cons list
enum List {
    Cons(i32, List),
    Nil,
}

// 错误： 确定计算List类型时，递归循环，无法计算类型大小
//let list = Cons(1, Cons(2, Cons(3, Nil)));

// 修改：
enum List {
    Cons(i32, Box<List>), //  Box<T> 指针大小确定
    Nil,
}

let list = Cons(1,
    Box::new(Cons(2,
        Box::new(Cons(3,
            Box::new(Nil))))));


// 解引用*
let x = 5;
let y = &x;  // y是x的引用类型

assert_eq!(5, x);
assert_eq!(5, *y);  // 与integer类型比较，需要解引用，将&{integer} 通过解引用符号* 转成与integer


// Box重载了解引用符号*，可以像引用一样使用 Box<T>
let x = 5;
let y = Box::new(x);

assert_eq!(5, x);
assert_eq!(5, *y);
// Box<dyn T>
trait Printable {
    fn stringify(&self) -> String;
}
impl Printable for i32 {
    fn stringify(&self) -> String { self.to_string() }
}
fn print(a: Box<dyn Printable>) {
    println!("{}", a.stringify());
}
print(Box::new(10) as Box<dyn Printable>);


//C++风格的单链表Node
struct Node {
    value: i32,
    // 使用Option,因为可能为NULL
    // 使用Box<T> 声明为指针类型
    next: Box<Option<Node>>,
}
let a = Node {
    value: 5,
    next: Box::new(None),
};
let b = Node {
    value: 10,
    // 注意：这里将变量a的所有权，移动给了b.next
    next: Box::new(Some(a)),
};
println!("b is {:?}", b);
// 因为所有权被移动，无法再使用变量a
// 同样的，也无法将变量a 传递给另一个变量c的next，以共享链表节点
// println!("a is {:?}", a);
// 为了共享，需要使用下面的Rc<T>
// 为了能够修改指针所指向的对象，需要使用RefCell<T>
// 因此一个共享的可修改的List节点定义如下
struct SharedNode {
    value: i32,
    next: Rc<RefCell<Option<SharedNode>>>,
}
// 节点node_a
let node_a = SharedNode {
    value: 5,
    next: Rc::new(RefCell::new(None)),
};
// 定义共享可修改的节点的指针a，指向node_a
let a = Rc::new(RefCell::new(Some(node_a)));
// 定义节点b，next赋值为a
let b = SharedNode {
    value: 10,
    next: Rc::clone(&a),
};
// 定义节点c，next赋值为a
let c = SharedNode {
    value: 20,
    next: Rc::clone(&a),
};
// *a 解引用成RefCell
// 通过RefCell的borrow_mut方法，返回一个可变的智能指针RefMut<T> x
// *x 解引用获得SharedNode类型对象，因为整个实例是可变的，所以可以修改value成员变量
if let Some(ref mut x) = *a.borrow_mut() {
    (*x).value += 10;
}

//实现双向链表时，为了避免循环引用，需要引入Weak<T> weak pointer
// 持有一个对象的非拥有引用,类似Rc<T>，但是 weak pointer 并不影响析构
struct DoubleNode {
  value: i32,
  next: Rc<RefCell<Option<DoubleNode>>>,
  prev: Weak<RefCell<Option<DoubleNode>>>,
}
```

###### Rc\<T> 引用计数

多所有权，允许共享值。应用场景，免数据拷贝。但是不能修改包裹的对象。

等价于C++中的shared pointer共享指针。

```Rust
// 共享的list 部分
let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));

let b = Cons(3, Rc::clone(&a)); // clone 只是增加引用计数
let c = Cons(4, Rc::clone(&a));
```



###### Arc\<T> 原子引用计数

原子引用计数，`Rc`的多线程版本。

- 可以跨线程传递，跨线程共享对象
  - Arc类型可以保证被共享的类型的生命周期，与运行时间最长的线程活得一样久
- 对包括的类型对象，无可变性要求



###### RefCell\<T>

`RefCell<T>` 代表其数据的唯一的所有权。用于在运行时，检查借用规则（任意时刻只有一个可变引用或者无数不可变引用，引用必须有效）。单线程场景。想要修改所指向的T对象。

区别：

- `Rc<T>` 允许相同数据有多个所有者；`Box<T>` 和 `RefCell<T>` 有单一所有者。
- `Box<T>` 允许在编译时执行不可变或可变借用检查；`Rc<T>`仅允许在编译时执行不可变借用检查；`RefCell<T>` 允许在运行时执行不可变或可变借用检查。
- 因为 `RefCell<T>` 允许在运行时执行可变借用检查，所以可以在即便 `RefCell<T>` 自身是不可变的情况下修改其内部的值。
  - 内部可变性（Interior mutability）
    - 如果一个类型可以通过共享引用&T来改变其内部数据，则该类型具有内部可变性。
  - 底层使用`UnsafeCell<T>`

```rust
let x = 5;
// x 是不可变的，无法可变的借用
//let y = &mut x;

pub trait Messenger {
    // send 方法 不可变
    fn send(&self, msg: &str);
}
use std::cell::RefCell;
struct MockMessenger {
    // 内部可变的指针
    sent_messages: RefCell<Vec<String>>,
}
impl MockMessenger {
    fn new() -> MockMessenger {
        MockMessenger { sent_messages: RefCell::new(vec![]) }
    }
}
impl Messenger for MockMessenger {
    fn send(&self, message: &str) {
        // self 是不可变的引用，但是对sent_messages进行了修改
        // borrow_mut 返回可变的指针
        // borrow 返回不可变的指针
        self.sent_messages.borrow_mut().push(String::from(message));
    }
}
```



###### Pin\<P> 

```rust
use std::pin::Pin;

pub struct Pin<P> {
    pointer: P,
}
```

> **Pin**是一个这样的智能指针，他内部包裹了另外一个指针**P**，并且只要**P**指针指向的内容（我们称为**T**）没有实现**Unpin**，则可以保证**T**永远不会被移动（move）。
>
> 一般用Pin<P<T>>表示，P是Pointer的缩写，T是Type的缩写
>
> **Pin**自身是一个智能指针，**impl**了**Deref**和**DerefMut**
>
> **Pin**包裹的内容只能是指针，不能是其他普通类型
>
> **Pin**具有“钉住”**T**不能移动的功能，只要**T** 没有实现**Unpin**（默认所有类型都实现了**Unpin**，除了async/await 被编译后的实现Future的结构体）

**PIn的引入，为了防止自引用结构体的move。** 使用Pin，用于编译时检查自引用结构体是否存在move，存在时报错。

推荐直接阅读[Rust的Pin与Unpin](https://folyd.com/blog/rust-pin-unpin/) 这篇文章

```rust
//Pin使用
// new, P指向的T是Unpin, Pin的”钉住“效果是不起作用，跟正常的指针一样
Pin::new()
// unsafe 方法
Pin::new_unchecked()
// Pin<&mut T> 栈上，Pin<Box<T>> 堆上

struct Test {
    a: String,
    b: *const String,
    _marker: PhantomPinned, // 实现!UnPin
}

let mut test1 = unsafe { Pin::new_unchecked(&mut Test::new("test1")) };
Test::init(test1.as_mut());

let mut test2 = unsafe { Pin::new_unchecked(&mut Test::new("test2")) };
Test::init(test2.as_mut());

println!("a: {}, b: {}", Test::a(test1.as_ref()), Test::b(test1.as_ref()));

// 取消注释会编译报错，
// std::mem::swap(test1.get_mut(), test2.get_mut());
println!("a: {}, b: {}", Test::a(test2.as_ref()), Test::b(test2.as_ref()));
```

备注：

在`Future` 引入自引用，是为了解决最初版本的Future，不能跨过**异步等待点**（await point）进行借用的问题。如果你要异步等待（await）某件事，你就不能在那个时候持有任何存活的引用。

但是，实际不需要在Executor和Waker间真正的move `Future` ，创建新的Future变量，持久句柄即可。没有move，那么就不会有自引用在move后，产生悬空指针的风险，或者指向非法地址。

而Pin的作用正是这目的，告诉编译器不能move Future，请检查。

#### 2.6.4 Aysnc/await

rust 提供的**异步并发**编程模型，允许在少量 OS 线程上运行大量并发任务，同时通过`async/await`语法保留普通同步编程的大部分外观。（OS线程池，无法满足大量IO密集型的工作负载）

- 使用async 声明 需要异步的函数
  - async函数由编译器生成的返回Future结果
    - `Future` 是一个用trait实现的状态机，必须在executor上执行。
      - 如`futures::executor::block_on()` 阻塞方式执行，传入的Future。
    - async函数，可以在子线程中调用例如` tokio::spawn(async { ///异步函数调用 });`

- 可以使用await异步的获取另一个Future返回的结果
  - await由编译器生成代码调用future的poll方法
  - await不阻塞当前线程，异步等待Future的执行
    - await 会触发异步函数的执行
    - await虽然是异步的，顺序编写的逻辑，但是还是串行的执行逻辑
      - 即A.await；print "xxx"; B.await；那么还是会先执行A，然后打印“xxx”，最后执行B
      - 但是我们可以使用一些执行器，让Future并行。
  - await也只能在`async` 声明的函数或者blocks中使用

```rust
use futures::executor::block_on;

async fn learn_song() -> Song { /* ... */ }
async fn sing_song(song: Song) { /* ... */ }
async fn dance() { /* ... */ }

// 同步阻塞模式
let song = block_on(learn_song()); // 先学唱歌，返回Song
block_on(sing_song(song)); // 然后，唱歌
block_on(dance()); //最后，跳舞

// 异步
async fn learn_and_sing() {
	// 还是需要先学唱歌，但是异步等待学会
    let song = learn_song().await;
    // 学会后，执行唱歌这首歌
    sing_song(song).await;
    // 由于学会歌和唱歌是异步的，执行learn_and_sing方法不会阻塞主线程，可以继续执行其他逻辑，如跳舞
    // 又保证了学歌，然后唱歌的同步逻辑
}
async fn async_main() {
    let f1 = learn_and_sing();
    let f2 = dance();
    // 这里的join，可以并发等待多个Future的执行
    // 如果f1 被block了，执行f2，反之亦然
    // 如果f1和f2都被block了，那么阻塞主线程，等待executor执行f1,f2
    // 学歌并唱歌，与跳舞可以同时进行
    futures::join!(f1, f2);
}
block_on(async_main());
```

对比：

**OS线程**：

- 适用于少量任务，因为线程会带来 CPU 和内存开销。线程之间的生成和切换非常昂贵，因为即使是空闲线程也会消耗系统资源。
- 线程池库，可以降低一些成本，但是依然还是存在。
- 优势，可以重用现有的同步代码

**Aync**：

- 显著降低CPU和内存开销，特别是对于具有大量IO绑定任务的工作负载，例如服务器和数据库。
- 可以拥有比OS线程多几个数量级的任务
- 缺点，由于异步函数生成的状态机以及每个可执行文件都捆绑了一个异步运行时，异步 Rust 会导致更大的二进制 blob？



##### 实现原理

**Future** 

`Future`trait是Rust异步编程的核心。

A`Future`是可以产生值（可能为空()）的异步计算。

```rust
// Future模型
trait SimpleFuture {
    // 输出类型
    type Output;
    // 拉取结果的方法poll，被轮询时需要执行的方法
    // wake方法，用于唤醒Pending的Future，重新调用poll
    // 使用wake，可以避免executor轮询所有的Future
    // 注意是一个old例子，用于解释Async/await最初实现原理，最新rust的Future tarit，
    //使用fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Self::Output>;
    fn poll(&mut self, wake: fn()) -> Poll<Self::Output>;
}
// poll方法返回结果类型
enum Poll<T> {
    Ready(T), // Future完成，返回结果
    Pending, // Future还不能完成，排队
}

//具体实现
pub struct SocketRead<'a> {
    socket: &'a Socket,
}
impl SimpleFuture for SocketRead<'_> {
    type Output = Vec<u8>;

    fn poll(&mut self, wake: fn()) -> Poll<Self::Output> {
        //检查socket状态
        if self.socket.has_data_to_read() {
            // socket有数据，读取结果
            Poll::Ready(self.socket.read_buf())
        } else {
            // socket无数据，注册wake
            // 在socket，有数据时，将会重新调用poll
            // 我们通过wake，来觉得下一次调用poll的时机，
            // 而不是让Executor，一直死循环的轮询Future，调用poll
            self.socket.set_readable_callback(wake);
            Poll::Pending
        }
    }
}
```

`Future` 是一个状态机，每次IO暂停点有有一个变体（variant），而每个变体都保存了恢复执行所需的状态。

这里变体，在实现上是枚举 `Poll<T>`。



**Waker** 任务唤醒

`Waker`提供了一种`wake()`方法，被用于告诉Excutor应该唤醒关联的任务。

```rust
// 计时器例子：
// 创建计时器时启动一个新线程，休眠所需的时间，然后在时间窗口过去后向计时器发出信号。
use std::{
    future::Future,
    pin::Pin,
    sync::{Arc, Mutex},
    task::{Context, Poll, Waker},
    thread,
    time::Duration,
};
pub struct TimerFuture {
    shared_state: Arc<Mutex<SharedState>>,
}
/// 计时器和等待线程的共享状态
struct SharedState {
    // 休眠时间是否达到
    completed: bool,
	// 任务唤醒器
    waker: Option<Waker>,
}

impl Future for TimerFuture {
    type Output = ();
    // Pin参考2.6.3 Pin小节
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let mut shared_state = self.shared_state.lock().unwrap();
        if shared_state.completed {
            Poll::Ready(())
        } else {
            // 克隆waker，使能够唤醒当前任务
            // TimerFuture可以在 executor上的任务之间移动，
            // 这可能导致陈旧的唤醒器指向错误的任务，从而阻止 `TimerFuture` 正确唤醒
            // TimerFuture可能被移动其他Waker上！
            shared_state.waker = Some(cx.waker().clone());
            Poll::Pending
        }
    }
}
impl TimerFuture {
    pub fn new(duration: Duration) -> Self {
        let shared_state = Arc::new(Mutex::new(SharedState {
            completed: false,
            waker: None,
        }));
        let thread_shared_state = shared_state.clone();
        // 启动线程
        thread::spawn(move || {
            thread::sleep(duration);
            let mut shared_state = thread_shared_state.lock().unwrap();
            // 设置休眠时间，已经达到
            shared_state.completed = true;
            // 通过waker唤醒轮询Future的任务
            if let Some(waker) = shared_state.waker.take() {
                waker.wake()
            }
        });
		// 返回一个Future结果，在线程完成后才会真正有结果
        TimerFuture { shared_state }
    }
}
```

**Executor**

顶层`async`函数返回的`Future`的poll的执行者。统一的管理大量的Future。

```rust
struct Executor {
    // 使用通道，来接收任务
    // 持有通道的Rev端
    ready_queue: Receiver<Arc<Task>>,
}
/// 发送新的Future 任务到通道
#[derive(Clone)]
struct Spawner {
    task_sender: SyncSender<Arc<Task>>,
}
impl Spawner {
    fn spawn(&self, future: impl Future<Output = ()> + 'static + Send) {
        let future = future.boxed();
        let task = Arc::new(Task {
            future: Mutex::new(Some(future)),
            task_sender: self.task_sender.clone(),
        });
        self.task_sender.send(task).expect("too many tasks queued");
    }
}
/// 管理Future的任务
struct Task {
    // 任务所持有的Future对象
    // Mutex用于互斥，生产可以使用UnsafeCell
    future: Mutex<Option<BoxFuture<'static, ()>>>,
    // 用以将Task自身放回通道，完成waker功能
    task_sender: SyncSender<Arc<Task>>,
}
// 唤醒者
impl ArcWake for Task {
    fn wake_by_ref(arc_self: &Arc<Self>) {
        // 通过将任务放回通道，来唤醒任务
        // executor会查询通道，然后完成再次poll Future
        let cloned = arc_self.clone();
        arc_self
            .task_sender
            .send(cloned)
            .expect("too many tasks queued");
    }
}
// 创建对象
fn new_executor_and_spawner() -> (Executor, Spawner) {
 	// 通道大小
    const MAX_QUEUED_TASKS: usize = 10_000;
    let (task_sender, ready_queue) = sync_channel(MAX_QUEUED_TASKS);
    (Executor { ready_queue }, Spawner { task_sender })
}
// Executor的逻辑
impl Executor {
    fn run(&self) {
        // 循环监听通道，接收Task
        while let Ok(task) = self.ready_queue.recv() {
            // 取出Future
            let mut future_slot = task.future.lock().unwrap();
            if let Some(mut future) = future_slot.take() {
                // 根据Task自身，创建waker
                let waker = waker_ref(&task);
                let context = &mut Context::from_waker(&*waker);
                // `BoxFuture<T>`是`Pin<Box<dyn Future<Output=T>+Send+'static>>`的别名
                if let Poll::Pending = future.as_mut().poll(context) {
                    //Pending状态的Future，将其放回Task
                    // 而Task自身是一个waker，会将自身放回通道
                    // 但是，waker什么时候调用wake_by_ref的？
                    *future_slot = Some(future);
                }
            }
        }
    }
}

fn main() {
    let (executor, spawner) = new_executor_and_spawner();

    // 发送一个Future
    spawner.spawn(async {
        // 依然是串行的执行下面的逻辑；
        // 整个代码块作为一个Future结果，不阻塞主线程spawner.spawn发送，不需要它执行完；
        // 并且事实上，创建一个Future，不会执行，只有发给Executor，Executor才会去执行它。
        println!("howdy!");
        // 等待2s后完成
        TimerFuture::new(Duration::new(2, 0)).await;
        println!("done!");
    });

    // 关闭通道的发送端
    drop(spawner);

    // 通过Executor执行Future
    // 结果打印 "howdy!", pause, 最后 "done!".
    executor.run();
}
```





问题：

跨.await的引用，例如在一个异步函数中获取锁。

简单的解决方案，使用`tokio::sync::Mutex` 异步互斥锁。



备注：

io密集型并发crate： tokio

cpu密集型并发crate：rayon



## 3. 系统学习



TODO:

[pingcap](https://github.com/pingcap)/[talent-plan](https://github.com/pingcap/talent-plan) rust 深入



## REF

- [Rust官网](https://www.rust-lang.org/zh-CN/)
- [github:rust-lang](https://github.com/rust-lang) rust语言学习，官方，（book，sync-book，rust-by-example，crate等）
- [Rust 程序设计语言-中文版](https://kaisery.github.io/trpl-zh-cn/#rust-程序设计语言) 推荐
- [通过例子学Rust](https://github.com/rust-lang-cn/rust-by-example-cn) 推荐
- [RustPrimer中文版](https://github.com/rustcc/RustPrimer) 推荐
- [深入浅出Rust异步编程之Tokio](https://zhuanlan.zhihu.com/p/107820568)
- [透过 Rust 探索系统的本原：编程语言](https://zhuanlan.zhihu.com/p/365905673)
- [Rust学习笔记_2021](https://github.com/xuesongbj/Rust-Notes/tree/main/Rust学习笔记_2021)
- [深入浅出Rust异步编程之Tokio](https://zhuanlan.zhihu.com/p/107820568) 
- [零成本异步I/O](https://zhuanlan.zhihu.com/p/97574385) 对于go/java使用绿色线程的分析,为什么后来取消绿色线程的实现（因为非零成本）
- [tokio 官方教程](https://tokio.rs/tokio/tutorial) 如何用tokio写一个redis服务的教程
- [rust async-book](https://rust-lang.github.io/async-book/01_getting_started/01_chapter.html) 推荐
- [books-futures-explained](https://cfsamson.github.io/books-futures-explained/)
- [Rust：智能指针](https://zhuanlan.zhihu.com/p/125770192) 从rust语言角度
- [【译】Rust与智能指针](https://zhuanlan.zhihu.com/p/265466916) 从完成类似用C++的一些数据结构（List）功能角度
- [【译】Arc 在 Rust 中是如何工作的](https://zhuanlan.zhihu.com/p/300971430)


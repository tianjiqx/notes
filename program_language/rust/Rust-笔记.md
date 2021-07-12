# Rust-笔记







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
  - Rust 朝 Future 模型发展， async/await 模型，以同步的方式和思维编写代码，但以异步方式执行。
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

- 编译速度很慢





## 1.3 生态、应用

#### 1.3.1 应用

作为高级系统级编程语言，其应用领域基本可以同时覆盖 C/CPP/Java/Go/Python 的应用领域。

官方主推的几个领域。

- WebAssembly
- 网络
- 嵌入式



##### **数据服务**

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





## 3. 系统学习



TODO:

[pingcap](https://github.com/pingcap)/[talent-plan](https://github.com/pingcap/talent-plan) rust 深入



## REF

- [Rust官网](https://www.rust-lang.org/zh-CN/)
- [Rust 程序设计语言-中文版](https://kaisery.github.io/trpl-zh-cn/#rust-程序设计语言)
- [通过例子学Rust](https://github.com/rust-lang-cn/rust-by-example-cn)
- [RustPrimer中文版](https://github.com/rustcc/RustPrimer)
- [深入浅出Rust异步编程之Tokio](https://zhuanlan.zhihu.com/p/107820568)
- [透过 Rust 探索系统的本原：编程语言](https://zhuanlan.zhihu.com/p/365905673)


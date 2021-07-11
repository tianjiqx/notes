# Apache Arrow

## 1. 整体

**概念**：

Apache Arrow 是一个跨语言的内存数据开发平台，用于构建处理和传输大型数据集的高性能应用程序。它旨在提高分析算法的性能以及**将数据从一种系统或编程语言转移到另一种系统或编程语言的效率**。

Apache Arrow 的一个关键组件是其**内存中列格式**，这是一种标准化的、与语言无关的规范，用于表示内存中结构化的、类似表格的数据集。支持平面，或者嵌套的自定义数据格式。

它还提供计算库和零拷贝流消息传递和进程间通信。

官方提供了基于arrow规范的十多种语言和系统的实现。



**柱状格式（Columnar Format）**：

- 扫描和迭代大块数据时最大限度地提高效率
- SIMD向量化操作

![](apache-arrow笔记图片/simd.png)

**节省SerDe**：

没有标准的列数据格式，每种数据库和语言都必须实现自己的内部数据格式，之前数据的相互联邦需要做昂贵的SerDe。还可能需要重写通用的算法（如果只是运算，这点感觉在SerDe成通用的数据类型如java object后，可以免除，但是代价是，必须经过SerDe后运算。这里应该是指原生系统而言，自己需要重复开发）。

Apache Arrow 由十多个开源项目开发者支持，包含 Calcite, Cassandra, Drill, Hadoop, HBase, Ibis, Impala, Kudu, Pandas, Parquet, Phoenix, Spark, 和 Storm等。

使用或支持 Arrow 的系统（目前更多的是为大数据分析系统OLAP）可以在它们之间以很少甚至免费的成本传输数据。

标准化的内存格式促进了算法库的重用，甚至可以跨语言重用。

![](apache-arrow笔记图片/copy.png)

![](apache-arrow笔记图片/shared.png)

**Arrow lib库**：

Arrow 项目包含的库使能够以多种语言处理 Arrow 柱状格式的数据。



## 2. 组件介绍

### 2.1 列存的内存格式Columnar Format规范

Columnar Format包括与语言无关的内存数据结构规范、元数据序列化以及用于序列化和通用数据传输的协议。

使用 Google 的[Flatbuffers](http://github.com/google/flatbuffers)项目进行元数据序列化。

柱状格式有一些主要特点：

- 顺序访问（扫描）的数据邻接
- O(1)（恒定时间）随机访问
- SIMD 和矢量化友好
- 无需“指针混淆”即可重定位，允许在共享内存中实现真正的零拷贝访问

#### **2.1.1 术语**

- **Array**或**Vector**：具有相同类型的已知长度值序列。

- **Slot**：某个特定数据类型数组中的单个逻辑值。
- **缓冲区**Buffer或**连续内存区域**：具有给定长度的顺序虚拟地址空间。
  - 任何字节都可以通过小于区域长度的单个指针偏移量到达。
- **物理布局**：数组的底层内存布局，不考虑任何值语义。
  - 例如，32 位有符号整数数组和 32 位浮点数组具有相同的布局。
- **父**和**孩子数组**：名字来表达嵌套式结构物理值数组之间的关系。
  - 例如，一个`List<T>`-type 的父数组有一个 T 类型的数组作为它的子数组。
- **原始类型**：没有子类型的数据类型。
  - 诸如固定位宽、可变大小二进制和空类型等类型。
- **嵌套类型**：一种数据类型，其完整结构取决于一个或多个其他子类型。
  - 两个完全指定的嵌套类型相等当且仅当它们的子类型相等。
  - 例如，`List<U>` 和`List<V>`是不同类型，如果U 和V 是不同的类型。
- **逻辑类型**：使用某种相同物理布局实现的面向应用程序的语义值类型。
  - 例如，Decimal 值在固定大小的二进制布局中存储为 16 字节。同样，字符串可以存储为`List<1-byte>`。时间戳可以存储为 64 位固定大小的布局。



#### **2.1.2 物理内存布局**

数组由一些元数据和数据定义：

- 一种逻辑数据类型。
- 缓冲区序列。
- 一个64 位有符号整数的长度。实际实现限制为 32 位长度。
- 一个64 位有符号整数的 null 计数。
- 一个（可选）的**dictionary**，用于字典编码的数组。

嵌套数组还具有一组或多组这些项的序列，称为**子数组**。

每个逻辑数据类型都有一个明确定义的物理布局。以下是 Arrow 定义的不同物理布局：

- **原始类型（固定大小）**：一个值序列，每个值都具有相同的字节或位宽
- **变长二进制字节类型**：一个值序列，每个值都具有可变字节长度。使用 32 位和 64 位长度编码支持此布局的两种变体。
- **固定大小List类型**：嵌套布局，其中每个值都具有相同数量的取自子数据类型的元素。
- **可变大小List类型**：嵌套布局，其中每个值都是取自子数据类型的可变长度值序列。使用 32 位和 64 位长度编码支持此布局的两种变体。
- **Struct**：一个嵌套布局，由一组命名的子**字段**组成，每个子**字段**的长度相同，但类型可能不同。
- **稀疏**和**密集Union类型**：表示一系列值的嵌套布局，每个值都可以具有从子数组类型集合中选择的类型。
- **Null**：所有空值的序列，具有空逻辑类型

Arrow 列式内存布局仅适用于***data***而不是 *metadata*。实现可以自由地以任何方便的形式表示内存中的元数据。我们使用[Flatbuffers](http://github.com/google/flatbuffers)以独立于实现的方式 处理元数据**序列化**。



#### **2.1.3 缓冲区对齐和填充**

使用 64 字节对齐和填充。

- 将保证通过对齐访问来检索数字数组中的元素。
- 在某些架构上，对齐有助于限制部分使用的缓存行。



#### 2.1.4 有效性位图

除了联合类型（稍后会详细介绍），都使用专用的内存缓冲区，称为有效性（或“空”）位图，对每个值槽的空或非空进行编码。使用[最低有效位 (LSB) 编号](https://en.wikipedia.org/wiki/Bit_numbering)，数组长度为6，位图长度是以8字节分组（8,16,24,32...），从右到到左映射整个数组。

 计算是否非null：`is_valid[j] -> bitmap[j / 8] & (1 << (j % 8))`



#### 2.1.5 示例

- 原始类型int32的数组[1, null, 2, 4, 8]的布局：

```
* Length: 5, Null count: 1
* Validity bitmap buffer:

  |Byte 0 (validity bitmap) | Bytes 1-63            |
  |-------------------------|-----------------------|
  | 00011101                | 0 (padding)           |

* Value Buffer:

  |Bytes 0-3   | Bytes 4-7   | Bytes 8-11  | Bytes 12-15 | Bytes 16-19 | Bytes 20-63 |
  |------------|-------------|-------------|-------------|-------------|-------------|
  | 1          | unspecified | 2           | 4           | 8           | unspecified |
```

- 可变大小List类型数组List<Int8>，[[12, -7, 25], null, [0, -127, 127, 50], []]的布局：

```
* Length: 4, Null count: 1
* Validity bitmap buffer:

  | Byte 0 (validity bitmap) | Bytes 1-63            |
  |--------------------------|-----------------------|
  | 00001101                 | 0 (padding)           |

* Offsets buffer (int32)

  | Bytes 0-3  | Bytes 4-7   | Bytes 8-11  | Bytes 12-15 | Bytes 16-19 | Bytes 20-63 |
  |------------|-------------|-------------|-------------|-------------|-------------|
  | 0          | 3           | 3           | 7           | 7           | unspecified |

* Values array (Int8array):
  * Length: 7,  Null count: 0
  * Validity bitmap buffer: Not required
  * Values buffer (int8)

    | Bytes 0-6                    | Bytes 7-63  |
    |------------------------------|-------------|
    | 12, -7, 25, 0, -127, 127, 50 | unspecified |
```

List<List<Int8>>，[   [[1, 2], [3, 4]],     [[5, 6, 7], null, [8]],     [[9, 10]]  ]：

```
* Length 3
* Nulls count: 0
* Validity bitmap buffer: Not required
* Offsets buffer (int32)

  | Bytes 0-3  | Bytes 4-7  | Bytes 8-11 | Bytes 12-15 | Bytes 16-63 |
  |------------|------------|------------|-------------|-------------|
  | 0          |  2         |  5         |  6          | unspecified |

* Values array (`List<Int8>`)
  * Length: 6, Null count: 1
  * Validity bitmap buffer:

    | Byte 0 (validity bitmap) | Bytes 1-63  |
    |--------------------------|-------------|
    | 00110111                 | 0 (padding) |

  * Offsets buffer (int32) 偏移的个数比数组长度多1

    | Bytes 0-27           | Bytes 28-63 |
    |----------------------|-------------|
    | 0, 2, 4, 7, 7, 8, 10 | unspecified |

  * Values array (Int8):
    * Length: 10, Null count: 0
    * Validity bitmap buffer: Not required

      | Bytes 0-9                     | Bytes 10-63 |
      |-------------------------------|-------------|
      | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | unspecified |
```

- Struct 数组Struct<VarBinary, Int32>，[{'joe', 1}, {null, 2}, null, {'mark', 4}]

```
* Length: 4, Null count: 1
* Validity bitmap buffer:

  |Byte 0 (validity bitmap) | Bytes 1-63            |
  |-------------------------|-----------------------|
  | 00001011                | 0 (padding)           |

* Children arrays:
  * field-0 array (`VarBinary`):
    * Length: 4, Null count: 2
    * Validity bitmap buffer:

      | Byte 0 (validity bitmap) | Bytes 1-63            |
      |--------------------------|-----------------------|
      | 00001001                 | 0 (padding)           |

    * Offsets buffer:

      | Bytes 0-19     |
      |----------------|
      | 0, 3, 3, 3, 7  |

     * Values array:
        * Length: 7, Null count: 0
        * Validity bitmap buffer: Not required

        * Value buffer:

          | Bytes 0-6      |
          |----------------|
          | joemark        |

  * field-1 array (int32 array):
    * Length: 4, Null count: 1
    * Validity bitmap buffer:

      | Byte 0 (validity bitmap) | Bytes 1-63            |
      |--------------------------|-----------------------|
      | 00001011                 | 0 (padding)           |

    * Value Buffer:

      |Bytes 0-3   | Bytes 4-7   | Bytes 8-11  | Bytes 12-15 | Bytes 16-63 |
      |------------|-------------|-------------|-------------|-------------|
      | 1          | 2           | unspecified | 4           | unspecified |
```

更多，参见[Arrow Columnar Format](https://arrow.apache.org/docs/format/Columnar.html)

缓冲区定义：

![](apache-arrow笔记图片/Snipaste_2021-07-11_00-40-50.png)



### 2.2 序列化和进程通信IPC

列格式序列化数据的原始单位是“记录批次record batch”。从语义上讲，一个记录批次是称为**字段**的数组的有序集合，每个字段的长度相同，但数据类型可能不同。

记录批次的字段名称和类型共同构成批次的**schema**。

- Schema
- RecordBatch
- DictionaryBatch

#### 2.2.1 封装的消息格式

它包括一个序列化的 Flatbuffer 类型以及一个可选的消息体。

- 一个 32 位连续指示符。该值`0xFFFFFFFF`指示有效消息。这个组件是在 0.15.0 版本中引入的，部分是为了解决 Flatbuffers 的 8 字节对齐要求
- 指示元数据大小的 32 位小端长度前缀
- 使用[Message.fbs 中](https://github.com/apache/arrow/blob/master/format/Message.fbs)`Message`定义的类型 的消息元数据
- 将字节填充到 8 字节边界
- 消息体，长度必须是8字节的倍数

```
<continuation: 0xFFFFFFFF>
<metadata_size: int32>
<metadata_flatbuffer: bytes>
<padding>
<message body>
```

`metadata_size`包括的`Message`大小加上填充。

`metadata_flatbuffer`

- 版本号
- 消息值（Schema`，`RecordBatch`或 `DictionaryBatch之一）
- 消息体的大小
- `custom_metadata`用于任何应用程序提供的元数据字段

消息类别：

- Schema消息
  - 有序的字段序列，类型元数据，不含有数据缓冲区。
- RecordBatch消息
  - 一个记录批次，对应一个字段的有序数组集合。
- DictionaryBatch消息
  - 使用字典编码的消息，消息带有字典id，根据字典id从schema中获取编码的字典，对照字典获取实际数据。





### 2.3 Flight RPC协议

基于 Arrow 数据的高性能数据服务的 RPC 框架，建立在[gRPC](https://grpc.io/)和[IPC 格式](https://arrow.apache.org/docs/format/IPC.html)之上。

Flight 定义了一组 RPC 方法，用于上传/下载数据、检索有关数据流的元数据、列出可用数据流以及实现特定于应用程序的 RPC 方法。

`FlightDescriptor` 数据流描述符标识，用来获取数据。可以自己构造或者`ListFlights`获取。

`GetFlightInfo(FlightDescriptor)`以获取`FlightInfo` 消息，其中包含有关数据所在位置的详细信息（以及其他元数据，如schma和数据集大小估计）。Flight 不要求数据与元数据位于同一服务器上。

`DoGet(Ticket)`以获取 Arrow 记录批次流。

`DoPut(FlightData)`并上传 Arrow 记录批次流。



### 2.4 库（如rust）

库包含的组件：

- 列存的数组/向量 和 类似表的容器(数据帧)，能够支持平面或嵌套的类型
- 快速、与语言无关的元数据消息传递层（使用 Google 的 Flatbuffers 库）
- 引用计数的堆外缓冲区内存管理，用于零拷贝内存共享和处理内存映射文件
- 本地和远程文件系统的 IO 接口
- 用于远程过程调用 (RPC) 和进程间通信 (IPC) 的自描述二进制线格式（流和批处理/类文件）
- 用于验证实现之间二进制兼容性的集成测试（例如，将数据从 Java 发送到 C++）
- 与其他内存数据结构之间的转换
- 各种广泛使用的文件格式（例如 Parquet、CSV）的读取器和写入器

Rust实现从arrow项目独立出来了，分别是[arrow-rs](https://github.com/apache/arrow-rs)（核心） 和 [arrow-datafusion](https://github.com/apache/arrow-datafusion) （DataFusion 和 Ballista组件）

四个箱子crate：

- Arrow： 核心功能，内存布局，数组，底层计算

- Parquet：支持parquet的读取和写入

- Arrow-flight：基于 gRPC 的协议，用于在进程之间交换 Arrow 数据

  - 特点：并行传输，允许数据同时流入或流出服务器集群

  - gRPC优化：

    - 生成 Protobuf 线格式以`FlightData`包含正在发送的 Arrow 记录批次，不需要中间内存复制和序列化
    - 从 Protobuf 表示重建 Arrow 记录批次， `FlightData`无需任何内存复制或反序列化

  - 基本请求类型： 

    - 握手，用于确定客户端是否被授权，在某些情况下，建立一个实现定义的会话令牌以用于未来的请求

    - **ListFlights**：返回可用数据流的列表

    - **GetSchema**：返回数据流的schema

    - **GetFlightInfo**：返回感兴趣的数据集的“访问计划”，可能需要使用多个数据流。请求可以指定参数。

    - **DoGet**：向客户端发送数据流

    - **DoPut** : 从客户端接收数据流

    - **DoAction**：通用函数调用，执行特定实现的操作并返回任何结果

    - **ListActions** : 返回可用操作类型的列表

      ![](apache-arrow笔记图片/20191014_flight_simple.png)

  - 水平扩展：并行与分区数据访问

    - `GetFlightInfo` 请求，对数据集的客户端请求返回一个**端点**列表，每个**端点**都包含一个服务器位置和一张**票据**，用于在`DoGet`请求中发送该服务器 以获得完整数据集的一部分

    - 多断点模式好处：

      - client可以并行请求给所有端点

      - 端点角色可变，部分处理`GetFlightInfo`请求，部分只做DoGet和DoPut请求处理。

        ![](apache-arrow笔记图片/20191014_flight_complex.png)

- DataFusion：支持SQL的内存查询引擎（join，窗口函数）

  - 

- Ballista：分布式查询执行

  - 





## REF

- [Apache Arrow官方](https://arrow.apache.org/overview/)
- [Apache Arrow 内存数据](https://www.cnblogs.com/smartloli/p/6367719.html)
- [Arrow Columnar Format](https://arrow.apache.org/docs/format/Columnar.html)
- [arrow-rs](https://github.com/apache/arrow-rs)
- [arrow博客汇总](https://arrow.apache.org/blog/)
- [Apache Arrow Flight 简介：快速数据传输框架](https://arrow.apache.org/blog/2019/10/13/introducing-arrow-flight/)
- [Ballista：Apache Arrow 的分布式调度器](https://arrow.apache.org/blog/2021/04/12/ballista-donation/)
- [DataFusion：Apache Arrow 的 Rust 原生查询引擎](https://arrow.apache.org/blog/2019/02/04/datafusion-donation/)
- [TiDB 源码阅读系列文章（十）Chunk 和执行框架简介](https://pingcap.com/blog-cn/tidb-source-code-reading-10/#tidb-%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%E7%B3%BB%E5%88%97%E6%96%87%E7%AB%A0%E5%8D%81chunk-%E5%92%8C%E6%89%A7%E8%A1%8C%E6%A1%86%E6%9E%B6%E7%AE%80%E4%BB%8B)














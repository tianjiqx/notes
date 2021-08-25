# Hadoop-笔记

[toc]

## 1. MapReduce的api比较

1) 接口变为抽象类。

接口，只定义接口方法，未提供实现。这有助于实现C++的多重继承，一个类可以实现很多接口，无需担心菱形继承，同名成员访问问题。

而抽象类，在类的泛化方面更据有优势，提供默认实现。继承类可以选择是否实现这些方法。具有良好的向后兼容性，当需要给抽象类添加性的方法时，只要新方法提供默认实现，继承类可以不必改动。

2) 上下文封装

将变量和函数封装为各种上下文conext类，使API具有更好的易用性和扩展性。

减少参数列表长度，便于修改参数。



## 2.回调机制





## 3. 配置



## 4.序列化与反序列化







## 5.压缩编码

编码，解码器-抽象工厂



## 6.RPC



PB机制





## 7.管理hadoop

### 7.1 fsimage和editslog

每个fsimage文件包含所有的目录和文件inode信息（完整原信息的检查点，可以很大），inode信息是文件或目录的元数据的内部描述方式。例如文件，包含，副本级别，修改时间，访问时间，访问权限，块大小，文件块。数据块信息在NN内存，DN加去集群时，NN向DN获取数据块索引信息，建立映射关系。

文件系统客户端执行的写操作（创建，移动文件），会被记录到编辑日志中。实现，由多个段文件组成，最新的edits log，文件名带有inprogress，唯一。写操作的对edits的修改是，事务性的，并且secondry NN的edits log也写成功后，提交事务。

`hdfs dfsamin -saveNamespce` 创建检查点，默认1小时。



## 8. NameNode 元信息管理

### 8.1 内存管理

NameNode常驻内存占用，是HDFS集群扩展性的关键。

内存全景

- Namespace
  - 保存目录树及每个目录/文件节点的属性。
  - 定期flush到持久化设备上，生成一个新的FsImage文件，用于重启时恢复。
  - 数据结构
    - INode构成的树
      - INodeDirectory
        - 大小：(24 + 96 + 44 + 48) ∗ dirNum + 8 ∗ num(total children) 
      - INodeFile
        - 大小： (24 + 96 + 48) ∗ fileNum + 8 ∗ num(total blocks) 
    - 子节点name有序存储，根据名字二分查找
- BlocksMap
  - DataNode的Block信息，作为BlockManager成员
  - 数据结构LightWeightGset<K,V> 链表实现的哈希表
  - 大小：16 + 24 + 2% ∗ JVM堆空间GB +（ 40 + 128 ）∗  num(total blocks) 
    - （16 + 24 直接忽略吧）
    - 1亿Block ~20GB
- NetworkTopology
  - DataNode网络拓扑结构，机架感知
- 其他（各种管理器）
  - LeaseManager

NameNode常驻内存主要被Namespace和BlockManager使用，二者使用占比分别接近50%。其它部分内存开销较小且相对固定，与Namespace和BlockManager相比基本可以忽略。



NN内存预估模型：

**Total = 198 ∗ num(Directory + Files) + 176 ∗ num(blocks) + 2% ∗ size(JVM Memory Size)**



NameNode的扩展性问题

- 重新启动时间变长
  - 元数据INode数超过2亿，Block数接近3亿，FsImage文件大小将接近到20GB
  - 加载FsImage数据需要~14min
  - Checkpoint需要~6min
  - 整个重启过程将持续~50min
- 性能下降
  - 元数据的增删改查性能
- NameNode JVM FGC风险
  - FGC频率增加
  - FGC时间增加且风险不可控（CMS内存回收算法）
    - 正常100GB内存回收，数s停顿
      - （会有100GB需要一下回收情况，大规模删除数据？）
    - 回收失败，降级到串行内存回收时，停顿时间将达到数百秒
  - 同时性能分析，难以调试



一些改进措施：

- 合并小文件
  - 减少inode，block数量
- 调整合适的BlockSize（默认128MB）
  - 大文件
- HDFS Federation方案
  - （应该是最推荐的方式）
  - 多个NN分担元信息管理负担。



### 8.2 重启

NameNode 流程

- 加载FSImage；
  - 28% 时间
- 回放EditLog；
  - 1%
- 执行CheckPoint（非必须步骤，结合实际情况和参数确定）；
  - 10%
- 收集所有DataNode的注册和数据块汇报
  - 61%



HDFS2.7,2.8的重启一些优化：

- fix 执行CheckPoint时不能处理BlockReport请求
- 推迟SBN（StandbyNameNode）每间隔1min全局计算和验证Quota值任务



优化后：

元数据总量540M（目录树240M，数据块300M），超过4K规模的集群上重启NameNode总时间~35min，其中加载FSImage耗时~15min，秒级回放EditLog，数据块汇报耗时~20min。



## REF

- [java反射机制](https://mp.weixin.qq.com/s?__biz=MzI1NDU0MTE1NA==&mid=2247483785&idx=1&sn=f696c8c49cb7ecce9818247683482a1c&chksm=e9c2ed84deb564925172b2dd78d307d4dc345fa313d3e44f01e84fa22ac5561b37aec5cbd5b4&scene=0#rd)  java核心技术卷1 5.7 

- hadoop 技术内幕common，mapreduce，yarn

- hadoop 权威指南4版

- [HDFS NameNode内存全景-美团](https://tech.meituan.com/2016/08/26/namenode.html)

- [HDFS NameNode内存详解-美团](https://tech.meituan.com/2016/12/09/namenode-memory-detail.html) 内存大小计算、预估方法

- [HDFS NameNode重启优化-美团](https://tech.meituan.com/2017/03/17/namenode-restart-optimization.html)


# Kafka笔记

[TOC]

## 1. 场景、架构和优缺点

参考笔记[大数据系统鉴赏](https://github.com/tianjiqx/notes/blob/master/big_data_system/大数据系统-鉴赏.md) kafka 小节。



接下来的内容，将从外围介绍，然后抵达kafka核心，数据存储broker。

## 2. 生产者Producer

内置java版(0.9以后)，第三方有go,c++,python等。

![](kafka笔记图片/Snipaste_2021-06-26_00-27-36.png)

### 2.1 工作流程

- producer用户主线程，将待发送的消息封装进ProduceRecord对象
- 序列化器，将ProduceRecord对象序列化后，发送给分区器partitioner
  - partitioner：用于划分消息被发送到主题的哪个分区。默认分区器时hash消息的key。无key轮询分区。
    - 并且确保相同的key在同一个分区。（TODO坏处：数据倾斜问题？）
    - 一个主题有多个分区，分区作为并行处理单元。
    - 分区在物理存储路径上对应一个目录，格式:${topicName}-${partitionId}
      - 分区目录下是该分区的日志段LogSegment，包括日志数据文件和两个索引文件。
        - 一个日志段对应一个日志文件，索引文件.index和.timeindex分别是消息偏移和消息时间戳索引文件
      - 分区数可以大于节点数，但是副本数不能大于节点数。
  - 用户可以跳过分区器自定义目标分区，或者自定义分区器。
  - 在客户端进行分区选择，比先发给broker端，然后broker路由到master减少一次网络传输开销
- 确定目标分区后，消息先进入到一个消息缓冲队列。
  - 先去队列最后一个位置，不存在或队列满，创建一个新的批记录，再加入队尾
- 另一个工作线程(I/O发送线程，Sender线程)负责实时的从缓存区提取消息，封装进一个batch，统一发送给对于的broker。
  - 目标broker是分区所在的leader副本的broker。
  - 按照节点发送（迭代所有分区，相同节点上的分区统一发送）
- 服务器收到消息后，写入成功，返回RecordMetaData 对象，包含主题，分区，消息在分区的偏移量offset。
  - 失败，生产者会尝试重试，超过重试次数，抛出异常。



生产者的api send方法发送给支持同步和异步两种。

- 同步：等待消息返回成功，发送下一条
  - 实现Futrue.get()
- 异步：直接发下一条，返回消息异步处理(如打印日志，错误重发等)。
  - 传递匿名回调类对象，处理返回结果。new Callbackuk(){}

生产者使用push模型，推送消息给broker。

**消息通信**

为了处理客户端与多个broker节点的消息通信，kafka使用java NIO的选择器模式

生产者客户端只需要使用一个选择器，就可以同时和Kafka集群的多个服务端进行网络通信（监听，轮询）。  

具体内容见kafka技术内幕2.1.4节。

Selector ---(SelectKey)-- SocketChannel (多)

![](kafka笔记图片/Snipaste_2021-06-26_16-05-23.png)

（星环BAR client连接master请求的改进，master备份，恢复，查询请求的处理分开）



### 2.2 无消息丢失配置

消息使用异步发送后，如果生产者宕机，但是消息还在缓冲队列里，就产生数据丢失问题。而同步发送性能太差。

```shell
##### producer端配置
# deprecated,max.block.ms替代了,缓冲区满后阻塞并停止接受新消息，但是不抛出异常
# block.on.buffer.full = true 
# 必须等待所有follower都响应发送消息后才能认为提交成功
acks = all
# 生产者无限重试,只重试可以恢复的异常
retries = MAX_VALUE
# 避免同分区消息乱序，避免消息乱序问题（消息发送顺序与实际存储顺序不一致）。
max.in.flight.requests.per.connection = 1
# 使用KafkaProducer.send(record, callback)
# callback逻辑中显式关闭producer：close(0) ，防止消息乱序
#####　broker端配置
# 不允许非ISR的副本选举为leader，避免broker端因日志水位截断导致消息丢失
unclean.leader.election.enable=false
replication.factor = 3
# 写入成功数
min.insync.replicas = 2
replication.factor > min.insync.replicas
# 消息处理完成之后再提交位移
enable.auto.commit=false
```



### 2.3 消息压缩

用CPU资源换取IO性能（磁盘和网络带宽）。

将一批消息压缩成一条发送，broker存储，消费者自动解压缩。

（更好的性能，Zstandard 压缩算法？）

推荐压缩算法LZ4。

（星环导入导出时，是使用gzip很好，数据量原因？）



性能提升：

多线程处理，推荐多线程多kafkaProducer实例，分区少可以单KafkaProducer。



## 3. 消费者Consumer

读取Kafka数据。自带java版本实现(0.9+)。

#### 消费者组

消费者组consumerGroup：topic的消息只会发送到订阅它的消费者组里面的一个消费者中。

topic的消费可以发送到多个消费者组。

group.id唯一标识一个consumer group。

消费者分组的作用：

- 容错，组内单一消费者挂掉不影响服务
- 提升性能，加快消费速度，横向扩展

(一定程度(分区级别，单个分区内)保证消息处理的顺序性)



![](kafka笔记图片/Snipaste_2021-06-26_15-08-13.png)

注意：组内消费者数量超过主题的分区数，将导致消费者闲置。

分区所有权从一个消费者转移到另一个消费者——再均衡rebalance。

根据分组的个数，消息模型可以分成：

- 队列模式：所有消费者在一个组里
- 发布/订阅模式：多个消费者组，消息被广播多次。消息平均分配给组里的消费者。

#### push vs. pull

消费者采用pull模式，从broker拉取数据。

- 如果使用broker push模式，缺点在于很难适配不同消费速率的消费者。提升push速度，容易产生拒绝服务和网络拥塞
- pull模式，可以根据消费者消费速度，精细调整。
- 此外，可以批处理消息。
- pull缺点，在于消费者轮询，可能盲等待。

消费端的位移offset，Kafka选择让consumerGroup 保存offset。也有checkpoint。

- broker 无消费者的状态，扩展性增强
- 无需消费者应答，确认消费者消费成功
- 无状态，减去存储压力

**消息轮询**

消费者的工作流程，是在一个无限循环中，处理群组协调，分区再平衡，发送心跳和获取数据。



**消费消息**

![](kafka笔记图片/Snipaste_2021-06-26_18-05-34.png)

详细见kafka技术内幕 第3，4章。

注意zk已经在2.8取消。

队列作为消息缓存。

![](kafka笔记图片/Snipaste_2021-06-26_18-11-53.png)

![](kafka笔记图片/Snipaste_2021-06-26_18-16-02.png)

（TODO 新旧API实现考量）



多消费者实现：

- 一个线程一个消费者kafkaConsumer
  - 简单，快，无线程交互开销，offset管理方便
  - socket开销，consumer数受限与分区数，broker端负载高
- 单consumer，多worker(线程池)
  - 消息获取与处理解耦；扩展性好
  - 分区内消息顺序处理问题难；线程异常导致消费数据丢失；offset管理问题





#### 提交

消费者更新分区当前位置的操作 。

broker不负责管理消息的消费情况。

而是kafka自定义了一个内部特殊主题_consumer_offset。消费者会向这个主题发送消息，消息包含每个分区的偏移量。

在消费者崩溃或者新的消费者加入群组，触发再平衡时。消费者可能被分配到新的分区。为了能继续处理新的分区，消费者读取这个分区最后一次提交的偏移量，然后从这里开始继续处理。

提交的偏移量小于客户端处理的最后一个消息的偏移量，导致消息会被重复处理。（相反大于，将导致消息丢失）

##### 自动提交

`enable.auto.commit=true` 默认每过5s。消费者将从poll接收到最大的偏移量提交。自动提交逻辑在轮询内。

缺点：可能重复处理消息。

缓解：减少时间间隔

##### 提交当前偏移量

`auto.commit.offset=false` 应用程序通过commitSync() 提交。

发生再均衡，还是存在消息重复处理。

并且提交时会阻塞，降低吞吐量。

##### 异步提交

commitASync() 不等待broker响应。无阻塞。支持回调方法。

##### 同步和异步组合提交

先异步，产生异常后再使用同步。同步失败，关闭消费者。

##### 提交特定偏移量

不按处理消息的批次频率，批次已处理的，更快提交。

批次中每处理n条(1000)就提交一次。



独立消费者，无需分区、再平衡。



## 4. 消息代理Broker

存储层。







## REF

#### 

- [ ] Kafka权威指南 （设计动机，如何推导出设计的）
- [ ] Kafka stream实战-(英) （kafka如何走向流处理）
- [ ] Kafka 技术内幕-郑奇煌 （源码分析，完整架构细节实现）
- [ ] Kafka源码解析与实战-王亮 (源码分析比例最重，分析源码时再看，与内幕相互补充)
- [ ] Apache Kafka 实战-胡夕 (kafka1.0.0，带有一定使用上的介绍) 


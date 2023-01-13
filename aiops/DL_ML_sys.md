## ML&DL系统

### WEKA

基于java实现的机器学习库，主要提供三类机器学习能力：

- 过滤， 数据预处理
- 分类
- 聚类

也提供评估，属性选择，从数据中删除不相关属性。



### Spark

### TensorFlow











### [分布式方法](https://openmlsys.github.io/chapter_distributed_training/methods.html)

- 数据并行，解决单节点的算力不足
  - 给定一个训练批**大小N**，并且希望使用M个并行设备运行，得到训练结果如剃度，训练程序利用平均梯度修正模型参数。
- 模型并行，解决单节点的内存不足
  - 场景：模型中含有大型算子，例如深度神经网络中需要计算大量分类的全连接层（Fully Connected Layer）
  - 假设这个算子具有**P个参数**，有N个设备，将P个参数平均分配给N个设备，能够在内存容量的限制下完成前向传播和反向传播中所需的计算。**算子内并行**（Intra-operator Parallelism）
- 混合并行
  - 混合使用数据并行和模型并行



## REF

- Books:
  - [Dataframe Systems: Theory, Architecture, and Implementation](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2021/EECS-2021-193.pdf)
  - 分布式机器学习：算法、理论与实践
  - [机器学习系统：设计和实现](https://openmlsys.github.io/)
  - [TensorFlow内核剖析](https://github.com/horance-liu/tensorflow-internals/blob/master/tensorflow-internals.pdf)


- Courses:
  - [深度学习系统dlsys](https://dlsyscourse.org/) 

> 本课程的目标是让学生了解和概述深度学习系统的“全栈”，从现代深度学习系统的高层建模设计，到自动微分工具的基本实现，再到底层高效算法的设备级实现。在整个课程中，学生将从头开始设计和构建一个完整的深度学习库，能够进行基于 GPU 的高效操作，自动微分所有已实现的功能，以及支持参数化层、损失函数、数据加载器和优化器的必要模块。使用这些工具，学生将构建几种最先进的建模方法，包括用于图像分类和分割的卷积网络，

- [MLOps课程](https://madewithml.com/courses/mlops/)

- [google 机器学习速成课程](https://developers.google.com/machine-learning/crash-course) 概念



- ml in java

  - [weka](https://waikato.github.io/weka-wiki/using_the_api/) 
  - [elki](https://github.com/elki-project/elki) ELKI 是一个用 Java 编写的开源 (AGPLv3) 数据挖掘软件。
  - 关注 **聚类**分析和**无监督异常值检测**。
  - [支持的算法列表](https://elki-project.github.io/algorithms/)
  - 根据`OutlierResult` 定义缺少预测值，上下界等。

  - [yahoo/egads](https://github.com/yahoo/egads)
    - 雅虎开源的 Java 包，用于自动检测大规模时间序列数据中的异常。

- [SREWorks](https://github.com/alibaba/SREWorks)

  - 阿里 云原生数智运维平台
  - [异常检测](https://github.com/alibaba/SREWorks/blob/main/saas/aiops/api/anomalydetection/README.md) 简单的基于超过 mean +/-  n * sigma 作为预测区间判断时间点是否异常。[code](https://github.com/alibaba/SREWorks/blob/main/saas/aiops/api/anomalydetection/AnomalyDetection/anomaly_detection.py)

- ts in dl
  - [预知未来——Gluon 时间序列工具包（GluonTS）](https://zh.mxnet.io/blog/gluon-ts-release) 


## ML&DL系统

### WEKA

基于java实现的机器学习库，主要提供三类机器学习能力：

- 过滤， 数据预处理
- 分类
- 聚类

也提供评估，属性选择，从数据中删除不相关属性。

### Spark

spark mllib

### Flink

- [flink-ml](https://github.com/apache/flink-ml)
- [docs](https://nightlies.apache.org/flink/flink-ml-docs-master/)
- [blog: Apache Flink ML 2.0.0 发布公告](https://developer.aliyun.com/article/851353)
  Checkpoint 机制, Exactly-Once 的容错
- [blog: Flink ML API，为实时机器学习设计的算法接口与迭代引擎](https://flink-learning.org.cn/article/detail/a0f69045967f9ca68736b518bd40a12a)

### ml on rust

- [GitHub - rust-ml/linfa: A Rust machine learning framework.](https://github.com/rust-ml/linfa)
- [eto-ai / lance](https://github.com/eto-ai/lance)
- 

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
  
  - [What is MLOps?](https://newrelic.com/blog/best-practices/what-is-mlops)

- [google 机器学习速成课程](https://developers.google.com/machine-learning/crash-course) 概念

- [aiops workshop](http://workshop.aiops.org/)

- ml in java
  
  - [weka](https://waikato.github.io/weka-wiki/using_the_api/)  
    
    - 过滤，分类，聚类算法，贝叶斯
  
  - [elki](https://github.com/elki-project/elki) ELKI 是一个用 Java 编写的开源 (AGPLv3) 数据挖掘软件。
    
    - 关注 **聚类**分析和**无监督异常值检测**。
    - [支持的算法列表](https://elki-project.github.io/algorithms/)
    - 根据`OutlierResult` 定义缺少预测值，上下界等。
  
  - [yahoo/egads](https://github.com/yahoo/egads)
    
    - 雅虎开源的 Java 包，用于自动检测大规模时间序列数据中的异常。

- [SREWorks](https://github.com/alibaba/SREWorks)
  
  - 阿里 云原生数智运维平台
  - [异常检测](https://github.com/alibaba/SREWorks/blob/main/saas/aiops/api/anomalydetection/README.md) 简单的基于超过 mean +/-  n * sigma 作为预测区间判断时间点是否异常。[code](https://github.com/alibaba/SREWorks/blob/main/saas/aiops/api/anomalydetection/AnomalyDetection/anomaly_detection.py)

- [Google BigQuery ML](https://cloud.google.com/bigquery-ml/docs/tutorials))

- [Google Vertex AI](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform?hl=zh-cn)
  
  - auto ml，输入训练用的tabular, image, text, or video data自动化的训练和评估模型
  
  - 自定义训练过程

- ts in dl
  
  - [预知未来——Gluon 时间序列工具包（GluonTS）](https://zh.mxnet.io/blog/gluon-ts-release) 

- [科普：分布式深度学习系统（一）](https://zhuanlan.zhihu.com/p/29032307)
  
  - [2](https://zhuanlan.zhihu.com/p/30976469)

- [ICML'22大模型技术Tutorial](https://zhuanlan.zhihu.com/p/562741952) ChatGPT

- [Top 10 Explainable AI Libraries (Python)](https://medium.com/geekculture/top-10-explainable-ai-libraries-python-71779e70058a)
  
  - 算法可解释性（参数权重）

- [Kaggle如何入门？ - 知乎](https://www.zhihu.com/question/23987009)

- [ML system 入坑指南 - Fazzie的文章 - 知乎](https://zhuanlan.zhihu.com/p/608318764)

- [DL Systems 学习指南](https://mp.weixin.qq.com/s/F8Dq6zmj6v4bR3WCKBgKAA)

- [PyTorch 源码解读系列](https://zhuanlan.zhihu.com/p/328674159)
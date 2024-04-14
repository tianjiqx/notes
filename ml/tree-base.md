
# 基于树模型的算法
基本思想很简单：提出一系列正交分割来基于特征上的if-else条件来创建决策边界，并对决策区域中的值使用聚合方法（如均值或众数）来预测结果-回归情况下的目标值和分类情况下的目标类。基于树的算法可以根据所使用的特定算法生成单个树或多个树。


## 特性

- Flexible灵活：基于树的算法可以捕获数据特征和输出之间的非线性关系
- Non-parametric非参数：这些方法不做任何关于其处理的基础数据的分布、独立性或恒定方差的假设。这对于那些对数据以及用于预测的功能知之甚少的应用程序至关重要。
- 更少的数据预处理要求：与基于距离的方法不同，这些算法不需要特征缩放，即在馈送到模型之前对数据进行归一化或标准化。
- 高度可解释性：由于决策区域是基于布尔关系产生的，因此这些方法可以图形化地可视化，以直观地理解算法的作用。


## 算法

### Decision trees 决策树

### Ensemble methods 集成方法

- Bagging 套袋
- Random forests 随机森林
- Boosting 提升
通过一系列的弱学习器的提升过程来构建一个强学习器。


## REF

- [tree-based-algorithms-in-machine-learning](https://www.omdena.com/blog/tree-based-algorithms-in-machine-learning)
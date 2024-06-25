
# ML 基础

## 概念

### 成本函数（Cost Functions）
成本函数是用来衡量模型预测结果与真实结果不一致的程度的一种方法。在机器学习中，我们通常希望找到一个模型，它的预测结果尽可能接近真实的数据。
成本函数的值越小，表示模型的预测结果与真实结果越接近，模型的性能越好。相反，成本函数的值越大，表示模型的预测结果与真实结果的差距越大，模型的性能越差。

在实际应用中，根据不同的问题和模型，我们可能会选择不同的成本函数。例如，在回归问题中，常用的成本函数有均方误差（Mean Squared Error, MSE）和平均绝对误差（Mean Absolute Error, MAE）等；在分类问题中，常用的成本函数有交叉熵损失（Cross-Entropy Loss）等。

分类：
-  Entropy 熵：度量数据中的不确定性或随机性。目标是最小化熵，以实现同质区域，即具有属于相似类的数据点的区域。

- Gini index 基尼系数：衡量随机选择的数据点被特定节点错误分类的可能性。

- Information Gain 信息增益：测量由于分裂而发生的熵/基尼指数的减少。基于树的算法使用熵或基尼指数作为标准来进行最“信息”的分割，即将标准减少最多的分割。

回归：
- 均方误差（Mean Squared Error, MSE）：测量区域中每个数据点的目标类与决策区域的平均响应之间的平方差之和。



### 损失函数（Loss Functions）
损失函数与成本函数类似，也是用来衡量模型预测结果与真实结果之间差异的一种方法。不过，**损失函数更侧重于单个样本的误差**，而成本函数则通常是对所有样本损失的平均或者总和。

损失函数的选择同样依赖于具体的问题类型。例如，在二分类问题中，我们可能会使用逻辑损失（Logistic Loss）；在多分类问题中，除了交叉熵损失外，还可能会使用Sigmoid Loss或者Softmax Loss等。

#### 区别与联系
- 范围：成本函数通常关注整个数据集的性能，而损失函数关注单个样本的性能。
计算方式：损失函数计算的是单个样本的误差，成本函数通常是损失函数在所有样本上的平均值或总和。
- 优化目标：在模型训练过程中，我们的目标是最小化成本函数，因为我们希望模型在整个数据集上都有良好的表现。

尽管成本函数和损失函数有所区别，但它们在实际应用中往往是相互关联的。在训练模型时，我们通常会首先计算每个样本的损失函数，然后通过某种方式（如平均）得到成本函数，最后通过梯度下降等优化算法来最小化成本函数，从而提高模型的性能。




## REF
- GPU 编程
    - [如何入门 OpenAI Triton 编程? - 董鑫的回答 - 知乎](https://www.zhihu.com/question/622685131/answer/3217107882)
    - [CUDA 编程的基本原理是什么? 怎么入门? - 董鑫的回答 - 知乎](https://www.zhihu.com/question/613405221/answer/3129776636)
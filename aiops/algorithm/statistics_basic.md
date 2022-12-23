# 统计基础

## 1.术语

- **期望（expected）**，又称均值。E(X)。
- **残差（residual）**指实际观察值与估计值（拟合值）之间的差。

- **离差（deviation）**即标志变动度，是观测值或估计量的平均值与真实值之间的差。

- **方差（variance）**衡量的是当我们对 *x* 依据它的概率分布进行采样时，随机变

  量 x 的函数值会呈现多大的差异。随机变量X与其均值的偏离程度。E[(X-E(X))^2]

  - D(X)=E(X^2)-[E(X)]^2。

- **标准差（standard deviation）** 方差（variance）的平方根。

- **协方差（covariance）** 在某种意义上给出了两个变量线性相关性的强度以及这些

  变量的尺度。

  - Cov（f(x),g(y)）=E[ f(x) -E(f(x)g(y)) -E(g(y))]

  - 如果协方差是正的，那么两个变量都倾向于同时取得相对较大的值。如果协方

    差是负的，那么其中一个变量倾向于取得相对较大的值的同时，另一个变量倾向于

    取得相对较小的值。

- **均方根（root mean square /rms）**







## 2.ML分类评估指标

- 混淆矩阵：
  - 四象限：TN,FP,FN,TP
    - T,F true，false 预测
    - N,P, negative，passive 实际
- 精确率 = TP / (TP + FP)
  - 用来评估在分类器所得正例结果中，真正正确的正例占该结果的多少。
- 召回率 = TP / (TP + FN) 
  - 召回率表示分类器正确找出来的正例，占样本实际正例的多少。
- F1 score  精确率和召回率的调和平均
  - 确度和召唤率往往是不可兼得的关系，不能既提高精确度又提高召回率。









## REF

- [线性回归（Linear Regression）和最小二乘法（ordinary least squares）](https://www.cnblogs.com/BlueBlue-Sky/p/9307220.html)

- 
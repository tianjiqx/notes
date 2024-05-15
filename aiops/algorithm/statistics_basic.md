# 统计基础

## 1.术语

- **期望（expected）**，又称均值。E(X)。

- **残差（residual）**指实际观察值与估计值（拟合值）之间的差。

- **离差（deviation）**即标志变动度，是观测值或估计量的平均值与真实值之间的差。

- **方差（variance）**衡量的是当我们对 *x* 依据它的概率分布进行采样时，随机变
  
  量 x 的函数值会呈现多大的差异。随机变量X与其均值的偏离程度。E[(X-E(X))^2]
  
  - D(X)=E(X^2)-[E(X)]^2。

- **标准差（standard deviation）** 方差（variance）的平方根。sigma

- **协方差（covariance）** 在某种意义上给出了两个变量线性相关性的强度以及这些
  
  变量的尺度。
  
  - Cov（f(x),g(y)）=E[ f(x) -E(f(x)g(y)) -E(g(y))]
  
  - 如果协方差是正的，那么两个变量都倾向于同时取得相对较大的值。如果协方
    
    差是负的，那么其中一个变量倾向于取得相对较大的值的同时，另一个变量倾向于
    
    取得相对较小的值。

- **均方根（root mean square /rms）**

- **Z-score 标准分数**  z = (x - u)/ \sigma\,  Z值的量代表着原始值和总体平均值之间的距离，原始值低于平均值时Z则为负数，反之则为正数。 一般在5-6 范围内。

- 差分
  
  - 一阶差分，当间距相等时，用下一个数值，减去上一个数值，就叫“一阶差分”
    
    - 意义，去除趋势性成分，将非平稳时间序列，平稳化stabilize 
  
  - 二阶差分，在一阶差分结果的基础上再次应用差分

## 2.ML分类评估指标

- 混淆矩阵：
  
  - 四象限：TN,FP,FN,TP
    - T,F true，false 预测正确或者错误
    - N,P, negative，passive 预测负例或者正例

- 准确率 Accuracy  ACC= (TP + TN) / 总样本（TN+FP+FN+TP）
  
  - 用来评估在预测正确的结果，占样本实际比例的多少。(预测在总样本中准确的比例)
  - 错误率 Error = 1 -  Accuracy

- 精确率 Precision = TP / (TP + FP) 
  
  - 用来评估在分类器所得正例结果中，真正正确的正例占该结果的多少。（预测结果中正确的比例）
  
  - 过杀率 FDR = FP / (TP + FP) = 1 - Precision 

- 召回率 Recall = TP / (TP + FN) 
  
  - 召回率表示分类器正确找出来的正例，占样本实际正例的多少。（发现问题的比例）
  - 也叫灵敏度Sensitivity，查全率，真正率。
  - 假负率FNR = FN / (TP + FN) = 1 - Recall ，漏检率，把正样本判断为负样本的在正样本中的比例。

- 特异度 Specificity = TN / (TN+FP)
  
  - 表示分类器正确找出来的负例，占样本实际负例的多少。
  
  - 也叫真负率。

- F1-score = 2(P*R)/(R+R) ， P精确率，R 召回率
  
  - F1-score 精确率和召回率的调和平均
  
  - 精确率和召唤率往往是不可兼得的关系，不能既提高精确率又提高召回率。

- ROC曲线和AUC值
  
  - (FPR， TPR)构成的描述ROC曲线， 横坐标FPR，纵坐标TPR，范围[0,1]。我们按这个范围设置污染度来描述样本中正例负例的比例，即可逐步绘制曲线。横坐标=1-Specificity，纵坐标Sensitivity、Recall。
  
  - AUC的含义为，当随机挑选一个正样本和一个负样本，根据当前的分类器计算得到的score将这个正样本排在负样本前面的概率。也代表ROC曲线下与坐标轴围成的面积。通常AUC的值介于0.5到1.0之间，较大的AUC代表了较好的性能。AUC=0.5 表示与随机猜测一致。

#### 相关性

https://zhuanlan.zhihu.com/p/27161877

## REF

- [线性回归（Linear Regression）和最小二乘法（ordinary least squares）](https://www.cnblogs.com/BlueBlue-Sky/p/9307220.html)

- [Practical Machine Learning](https://c.d2l.ai/stanford-cs329p/)

- [4.4.2分类模型评判指标（一） - 混淆矩阵(Confusion Matrix)_](https://blog.csdn.net/Orange_Spotty_Cat/article/details/80520839)

- [机器学习-基础知识- TP, FN, FP, TN - 又见苍岚](https://www.zywvvd.com/notes/study/machine-learning/basic-knowledge/TP-FN-FP-TN/Evaluation-index/)

- [机器学习-基础知识 - Precision, Recall, Sensitivity, Specificity, Accuracy, FNR, FPR, TPR, TNR, F1 Score, Bal](https://cloud.tencent.com/developer/article/2066696)

- [什么是ROC曲线？为什么要使用ROC?以及 AUC的计算](https://cloud.tencent.com/developer/article/1747389)  AUC值越大，模型的分类效果越好, 相同AUC值，根据需要的Sensitivity和Speciticity不同，评价不同模型。

- [在机器学习中AUC和accuracy有什么内在关系](https://www.zhihu.com/question/313042288)
  
  - AUC对应的是一系列的acc，acc是衡量的是一个模型在一个特定threshold下的预测准确度

- [平稳性和差分](https://otexts.com/fppcn/stationarity.html)

- [几种常见的聚类外部评价指标](https://zhuanlan.zhihu.com/p/343667804)
- [评价聚类的指标：纯度、兰德系数以及调整兰德系数](https://www.jianshu.com/p/13cff7c11669) 混淆矩阵的计算
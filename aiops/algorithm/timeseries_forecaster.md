## 时序预测

### 时序异常分类

- innovational outlier (IO):造成离群点干扰不仅作用于X(T)，而且影响T时刻以后序列的所有观察值。
- additive outlier (AO):造成这种离群点的干扰，只影响该干扰发生的那一个时刻T上的序列值，而不影响该时刻以后的序列值。
- level shift (LS):造成这种离群点的干扰是在某一时刻T，系统的结构发生了变化，并持续影响T时刻以后的所有行为，在数列上往往表现出T时刻前后的序列均值发生水平位移。
- temporary change (TC)：造成这种离群点的干扰是在T时刻干扰发生时具有一定初始效应，以后随时间根据衰减因子的大小呈指数衰减。

![img](ts_images/outlier.png)

阿里SLS对应用角度异常划分:

- 延时的毛刺、IO毛刺，存在**局部**峰值
- 业务系统调用量异常（断间隔的上升或下降）
  - 短时连续的IO类型异常
- 水位上升，新版本发布后，各个指标的形态与历史吻合，但是整体的平均水位有拔高
  - LS 类型异常

异常类型：

- 异常值（Outlier）
  - 给定输入时间序列x，异常值是时间戳值对$(t,x_t)$，其中观测值$x_t$与该时间序列的期望值$(E(x_t))$不同。
- 波动点（Change Point）
  - 给定输入时间序列x，波动点是指在某个时间t，其状态在这个时间序列上表现出与t前后的值不同的特性。
- 断层异常（Breakout）
  - 时序系统中某一时刻的值比前一时刻的值陡增或者陡降很多。
  - LS 类型异常
- 异常时间序列（Anomalous Time Series）
  - 给定一组时间序列$X={x_i}$，异常时间序列$x_i \in X$是在X上与大多数时间序列值不一致的部分。

### 时序预处理

- 推断时间间隔频率freq
  - 计算时间列最小的时间间隔作为时间频率(但是可以真实按M，Y设置频率)
    - 间隔28-31 day的时间转为'M'
    - 间隔365-366 day的时间转为'Y'
- 异常值处理
- 补点padding
  - 填充缺失时间间隔
- 缺失值插值
  - linear：线性
    - 对于首部的na值，使用后面一个合法观测值代替，而末尾na值，使用前面一个合法观测值代替。
  - spline：三次样条插值。
    - 相对于线性插值保持趋势，而对于末尾值，使用线性插值。
  - nearest： 最近邻。
    - 缺失值选择最近索引的值，首尾null值使用第一个最近的合法观测值代替。
  - last：最后值。
    - 假设缺失值的增量为0，首尾null值使用第一个最近的合法观测值代替。
  - zero：填零。

离异值识别：

- MAP绝对值差中位数法（Median Absolute Deviation）
  - 支持对AO，大部分IO，TC异常值进行预处理。
    - LF的处理？时间序列异常点及突变点的检测算法
  - 删除离异点，之后可以使用线性，插值
- 3-Sigma拉依达准则
  - 假设一组检测数据只含有随机误差，对原始数据进行计算处理得到标准差，然后按一定的概率确定一个区间，认为误差超过这个区间的就属于异常值。
    - 支持对AO的检测，大部分IO，TC。
      - 前提是数据服从正态分布
      - 反例，线性递增。

#### 标准化处理

- MinMaxScaler() 缩放到0和1之间
  
  - **Min-Max** **(Minimum and Maximum normalisation)** 
  
  - min-max归一化
  
  - 所有值等重要性，但测量误差膨胀，对异常值敏感

- StandardScaler() 缩放到均值为0，方差为1  **Mean-Std (Mean and standard deviation normalisation)**:
  
  - z-score归一化
  - 所有值等重要性，但测量误差膨胀

- MaxAbsScaler() 缩放到-1和1之间

- Normalizer() 缩放到0和1之间，保留原始数据的分布
  
  - 关注方向而忽略数值上的差异

影响：

- 基于距离的算法，量纲影响

- 剃度下降，收敛性

##### REF

- [标准化和归一化什么区别？](https://www.zhihu.com/question/20467170)
  
  - [标准化和归一化什么区别？ - 本空的回答](https://www.zhihu.com/question/20467170/answer/839255695)
  - [标准化和归一化什么区别？ - 夏洛克江沪川的回答 - 知乎](https://www.zhihu.com/question/20467170/answer/866038654)

- [异常检测：为什么要进行数据标准化? - 林德博格的文章 - 知乎](https://zhuanlan.zhihu.com/p/373562721)

- [scikit-learn数据预处理之特征缩放 - 迷路的文章 - 知乎](https://zhuanlan.zhihu.com/p/454711078)

- [API 参考-scikit-learn中文社区](https://scikit-learn.org.cn/lists/3.html)
  
  - RobustScaler() 基于四分位数的范围放缩数据，不保证范围[-1,1]

### 算法

#### ARIMA

AR

- pdq : 非季节性
  - p : AR 项， 自相关性
  - d ： 差分阶数
  - q :  移动平均项

MA

- PDQ: 周期内季节性
  - s：周期样本数

#### Exponential smoothing

20世纪50年代末提出了指数平滑法（Brown，1959;霍尔特，1957年; Winters，1960），并激发了一些最成功的预测方法。使用指数平滑法生成的预测是过去观测值的加权平均值，权重随着观测值的老化而呈指数衰减。换句话说，观察越近，关联的权重越高。该框架可以快速生成可靠的预测，并且适用于广泛的时间序列，这是一个很大的优势，对于工业应用具有重要意义。

基于预测算法的异常检测anomalies，使用sktime支持过去训练样本范围和区间预测的算法

- AutoETS
  - 时间相对ExponentialSmoothing 有50ms
- PMDARIMA
  - 缺点：PMDARIMA 第一个周期预测不准，上下界也很高
- StatsForecastAutoARIMA
  - 缺点：耗时相对较高  1s以上

## 时间序列异常检测

- 单变量时间序列
  
  - 估计
  
  - 预测（不使用当前数据）

- 多变量时间序列
  
  - 单变量（包括预处理，pca类似降维，再独立应用单指标异常检测）
  
  - 多变量

### REF

- Blázquez-García, Ane, et al. “A Review on Outlier/Anomaly Detection in Time Series Data.” ACM Computing Surveys, Apr. 2021, pp. 1–33, https://doi.org/10.1145/3444690.

- ADBench：[异常检测--ADBench (NeurIPS'22) is ALL You Need](https://zhuanlan.zhihu.com/p/565458918)
  
  - LOF在检测局部异常上遥遥领先其他算法，kNN在检测全局异常是显著的最强

- [论文分享：Revisiting Time Series Outlier Detection: Definitions and Benchmarks](https://zhuanlan.zhihu.com/p/602477997)
  
  - AR在检测上下文和形状异常值方面优于所有其他算法；OCSVM和iForest在多变量设置下的全局异常值和多个异常值方面优于REST；不和谐分析算法在季节性和趋势性异常值任务中表现最好。

## Q&A

### 1.预测未来时，区间预测的上下界经常看到开口越来越大

一般地，区间预测，基于标准差、方差乘以正态分布、t分布的百分比点值，来进行进行计算上下界。而方差或者[边际方差(marginal variance)](https://web.ma.utexas.edu/users/mks/384G06/condmargmeanvar.pdf)  `Var(Y) = E([Y - E(Y)]^2)`  ， 进行预测时，考虑到预测误差的累积，会相对预测水平而对标准差做一定调整，预测越远，标准差越大，从而开口越大。

例如，sktime STL Drift 是将趋势的方差乘以了系数，参考[多步预测](https://otexts.com/fpp3/prediction-intervals.html) 调整周期长度，从而降低Drift的方差的增长次数，缩小上下界开口。

## REF

- [wiki:ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average)

- [course: stat510](https://online.stat.psu.edu/stat510/) 宾夕法尼亚州立大学 应用时间序列分析 (网页更现代)

- [course: duke 411](https://people.duke.edu/~rnau/411home.htm) 杜克大学 统计预测： 回归和时间序列分析的注释

- **[预测： 方法与实践](https://otexts.com/fppcn/)  预测原理和实践中文版，第二版**
  
  - [预测区间](https://otexts.com/fppcn/prediction-intervals.html) 一步预测区间/多步

- [预测原理和实践（Rob Hyndman 和 George Athanasopoulos 的基于 R 的在线教科书）](https://www.otexts.org/fpp)第二版

- [Forecasting: Principles and Practice (3rd ed)](https://otexts.com/fpp3/) 预测原理和实践第3版

- [OpenIntro Statistics（David Diez、Christopher Barr、Mine Cetinkaya-Rundel）](https://www.openintro.org/stat/textbook.php?stat_book=os)

- [Online StatBook (David Lane)](http://onlinestatbook.com/2/index.html)
  
  - [International Institute of Forecasters](https://forecasters.org/resources/) 国际预测研讨会资源
  - [预测原理网站（J. Scott Armstrong 和 Kesten Green）](http://www.forecastingprinciples.com/)

- [刘岩-时间序列2018](http://www.liuyanecon.com/ug-ts-2018/)

- sktime
  
  - [AutoARIMA](https://www.sktime.org/en/stable/api_reference/auto_generated/sktime.forecasting.arima.AutoARIMA.html)
  - [ARIMA](https://www.sktime.org/en/stable/api_reference/auto_generated/sktime.forecasting.arima.ARIMA.html)

- [statsmodels.tsa.arima.model.ARIMA](https://www.statsmodels.org/devel/generated/statsmodels.tsa.arima.model.ARIMA.html)

- [PMDARIMA](http://alkaline-ml.com/pmdarima/)
  
  - [ARGS](https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.ARIMA.html#pmdarima.arima.ARIMA)

- [Anomaly-Detection-Using-ARIMA](https://github.com/atuljha23/Anomaly-Detection-Using-ARIMA)
  
  - https://github.com/atuljha23/Anomaly-Detection-Using-ARIMA/blob/master/Anomaly%20Detection%20Using%20ARIMA%20and%20Linear%20Regression.ipynb

- 模型解释
  
  - [使用 AIC、BIC 和 MDL 进行概率模型选择](https://machinelearningmastery.com/probabilistic-model-selection-measures/)
  - [如何解释 ARIMA 结果](https://analyzingalpha.com/interpret-arima-results)
  - [Statsmodel线性回归模型总结的简单解释](https://towardsdatascience.com/simple-explanation-of-statsmodel-linear-regression-model-summary-35961919868b)
  - [回归模型的评价指标比较](https://zhuanlan.zhihu.com/p/143169742)

- [分位数回归和预测区间](https://medium.com/analytics-vidhya/quantile-regression-and-prediction-intervals-e4a6a33634b4)

- [Time Series Analysis, Regression and Forecasting with tutiorials in python ](https://timeseriesreasoning.com/) Sachin Date

- 时序异常检测blogs
  
  - [异常检测综述](https://www.huhuapin.cn/2021/06/27/time-series-anomalies-detection/)
    
    - 异常分类，常见处理方法
  
  - [时间序列异常检测算法综述](https://www.biaodianfu.com/timeseries-anomaly-detection.html)
  
  - [时序异常检测算法概览](https://zhuanlan.zhihu.com/p/43413564)
  
  - [SLS机器学习介绍（03）：时序异常检测建模](https://developer.aliyun.com/article/669164)
  
  - [在R中使用异常化检测异常](https://www.srcmini.com/45906.html)
  
  - [异常检测：数据异常的类型(Types of Anomalies) - 林德博格的文章 - 知乎](https://zhuanlan.zhihu.com/p/340129272)

- 时序预处理
  
  - [预测:方法与实践-处理缺失值和离群值](https://otexts.com/fppcn/missing-outliers.html#missing-outliers)
  - [Pre-processing of Time Series Data](https://medium.com/enjoy-algorithm/pre-processing-of-time-series-data-c50f8a3e7a98)
  - [机器学习（三）：数据预处理--数据预处理的基本方法](https://zhuanlan.zhihu.com/p/100442371)
  - [多元时间序列缺失值处理方法总结](https://zhuanlan.zhihu.com/p/95459445)

- Datadog的算法
  
  - 异常检测outliers
    - [DBSCAN和MAP](https://www.datadoghq.com/blog/outlier-detection-algorithms-at-datadog/#toc-dbscan) 时间序列之间的异常划分
    - [扩展](https://www.datadoghq.com/blog/scaling-outlier-algorithms/) 而考虑到指标的整体幅度，上下文的意义，避免误报。

- [时间序列预测方法总结](https://zhuanlan.zhihu.com/p/67832773)

- [甩掉容量规划炸弹：用 AHPA 实现 Kubernetes 智能弹性伸缩](https://developer.aliyun.com/article/1078370)
  
  - *RobustPeriod*  周期识别
    - https://github.com/ariaghora/robust-period 非官方实现
  - *RobustSTL* 鲁棒的趋势，周期性分解
    - https://github.com/LeeDoYup/RobustSTL 非官方实现
      - 双边滤波降噪
      - 最小绝对偏差LAD 提取趋势

- 学时间序列分析有没有浅显易懂的书或视频？ - 张戎的回答 - 知乎 https://www.zhihu.com/question/280025347/answer/606794881

- 有什么好的关于时间序列分析的学习资料？ - Python与数据挖掘的回答 - 知乎 https://www.zhihu.com/question/26531019/answer/2688199336

- 时间序列笔记-专栏目录 - 冷泉望海遥的文章 - 知乎 https://zhuanlan.zhihu.com/p/374081618

- https://machinelearningmastery.com/start-here/#timeseries

- [机器学习笔记： 时间序列 分解 STL](https://blog.csdn.net/qq_40206371/article/details/122953379)

- [智能运维 | 故障诊断与根因分析论文一览](https://mp.weixin.qq.com/s/ILXnXQulDVFwmHdNtEcXng)

- [智能运维系列（二）| 智能化监控领域探索](https://mp.weixin.qq.com/s?__biz=MzIyOTYyNjMyNg==&mid=2247486650&idx=1&sn=7fef017e6a018eec6e72c890f85b683f)

- [alibi dectect](https://docs.seldon.io/projects/alibi-detect/en/latest/)
  
  - 开源 Python 库，专注于**异常值**、**对抗性**和**漂移**检测。
  - 大多数返回是否异常，以及异常分数， 基于正常，离群的比例，设置阈值。
  - 支持动态区间预测算法：仅prophet

- [时间序列发现周期的3种方式](https://medium.com/@shashindra3/three-ways-to-find-the-period-of-a-timeseries-251a6c8c4a3e)

- [如何处理类别型特征？](https://zhuanlan.zhihu.com/p/90782025)
  
  - One-hot 编码

- [【时间序列】时间序列预测算法总结](https://zhuanlan.zhihu.com/p/421710621)


- [tods](https://github.com/datamllab/tods/blob/master/README.zh-CN.md)



- 异常检测 blog：
  
  - https://towardsdatascience.com/well-log-data-outlier-detection-with-machine-learning-a19cafc5ea37 异常检测方法的一些范例
  
  - https://www.projectpro.io/article/anomaly-detection-using-machine-learning-in-python-with-example/555

- [日志服务用户成长集合页面](https://promotion.aliyun.com/ntms/act/logdoclist.html?spm=a2c6h.12873639.article-detail.15.bf1926cdblWG2U) 阿里云SLS demo 集合
  
  - [aiops 异常检测demo](https://sls4service.console.aliyun.com/lognext/project/dashboard-demo/dashboard/dashboard-1539675149912-481923?isShare=true&hideTopbar=true&hideSidebar=true)

- [Getting started with anomaly detection | Machine Learning in the Elastic Stack [8.6] | Elastic](https://www.elastic.co/guide/en/machine-learning/current/ml-getting-started.html)

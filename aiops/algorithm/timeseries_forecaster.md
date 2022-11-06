## 时序预测



### 时序异常分类





### 时序预处理

- 推断时间间隔频率freq
  - 计算时间列最小的时间间隔作为时间频率
    - 间隔28-31 day的时间转为'M'
    - 间隔365-366 day的时间转为'Y'
- 异常值处理
  - 识别删除后，插值（）
- 补点padding
  - 填充缺失时间间隔
- 缺失值插值



1667274898000  2022-11-01 11:54:58



### ARIMA

AR

- pdq : 非季节性
  - p : AR 项， 自相关性
  - d ： 差分阶数
  - q :  移动平均项

MA

- PDQ: 周期内季节性
  - s：周期样本数



### Exponential smoothing

20世纪50年代末提出了指数平滑法（Brown，1959;霍尔特，1957年; Winters，1960），并激发了一些最成功的预测方法。使用指数平滑法生成的预测是过去观测值的加权平均值，权重随着观测值的老化而呈指数衰减。换句话说，观察越近，关联的权重越高。该框架可以快速生成可靠的预测，并且适用于广泛的时间序列，这是一个很大的优势，对于工业应用具有重要意义。







基于预测算法的异常检测anomalies，使用sktime支持过去训练样本范围和区间预测的算法

- AutoETS
  - 时间相对ExponentialSmoothing 有50ms
- PMDARIMA
  - 缺点：PMDARIMA 第一个周期预测不准，上下界也很高
- StatsForecastAutoARIMA
  - 缺点：耗时相对较高  1s以上





### REF

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
- sktime
  - [AutoARIMA](https://www.sktime.org/en/stable/api_reference/auto_generated/sktime.forecasting.arima.AutoARIMA.html)
  - [ARIMA](https://www.sktime.org/en/stable/api_reference/auto_generated/sktime.forecasting.arima.ARIMA.html)
- [statsmodels.tsa.arima.model.ARIMA](https://www.statsmodels.org/devel/generated/statsmodels.tsa.arima.model.ARIMA.html)
- [PMDARIMA](http://alkaline-ml.com/pmdarima/)
  - [ARGS](https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.ARIMA.html#pmdarima.arima.ARIMA)
- 模型解释
  - [使用 AIC、BIC 和 MDL 进行概率模型选择](https://machinelearningmastery.com/probabilistic-model-selection-measures/)
  - [如何解释 ARIMA 结果](https://analyzingalpha.com/interpret-arima-results)
  - [Statsmodel线性回归模型总结的简单解释](https://towardsdatascience.com/simple-explanation-of-statsmodel-linear-regression-model-summary-35961919868b)
  - [回归模型的评价指标比较](https://zhuanlan.zhihu.com/p/143169742)
- [分位数回归和预测区间](https://medium.com/analytics-vidhya/quantile-regression-and-prediction-intervals-e4a6a33634b4)
- [Time Series Analysis, Regression and Forecasting with tutiorials in python ](https://timeseriesreasoning.com/) Sachin Date
- 时序异常检测blogs
  - [异常检测综述](https://www.huhuapin.cn/2021/06/27/time-series-anomalies-detection/)
  - [时间序列异常检测算法综述](https://www.biaodianfu.com/timeseries-anomaly-detection.html)
  - [时序异常检测算法概览](https://zhuanlan.zhihu.com/p/43413564)
  - [SLS机器学习介绍（03）：时序异常检测建模](https://developer.aliyun.com/article/669164)
  - [在R中使用异常化检测异常](https://www.srcmini.com/45906.html)

- 时序预处理
  - [预测:方法与实践-处理缺失值和离群值](https://otexts.com/fppcn/missing-outliers.html#missing-outliers)
  - [Pre-processing of Time Series Data](https://medium.com/enjoy-algorithm/pre-processing-of-time-series-data-c50f8a3e7a98)



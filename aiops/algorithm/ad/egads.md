

## 数据集
该数据集作为 Yahoo! 的一部分提供 Web 领域程序。 该数据集由带有标记异常点的真实和合成时间序列组成。 合成数据集由具有不同趋势、噪声和季节性的时间序列组成。 真实数据集由代表各种雅虎服务指标的时间序列组成。
A1Benchmark 基于一些雅虎服务器的实际生产流量。 其他 3 个基准基于合成时间序列。 


A2 和 A3 基准包括outliers，而 A4 基准包括变化点异常change-point anomalies。 合成数据集包含具有随机季节性、趋势和噪声的时间序列。 合成数据集中的异常值被插入到随机位置。


## EADS

在本文中，我们介绍了在Yahoo实现的通用异常检测系统EADS，它可以针对从故障检测到入侵检测的不同用例，自动监控和警告数百万个关于Yahoo不同属性的时间序列。正如我们在文章中所描述的，在Hadoop上的EADS的并行架构以及其通过Storm的流处理机制使其能够在Yahoo的数百万个时间序列上执行实时异常检测。


此外，EADS使用不同的时间序列建模和异常检测算法来处理不同的监控用例。通过将这一系列算法与机器学习机制结合在警报模块中，EADS自动适应对用户重要的异常检测用例。所有这些功能有效地创建了一个功能强大的异常检测框架，该框架既具有通用性，又具有可伸缩性。我们在真实数据集和合成数据集上的展示实验表明，与其竞争对手的解决方案相比，我们的框架具有更好的适用性。

## REF

- [yahoo/egads](https://github.com/yahoo/egads) github java实现了一些模型，比如指数平滑，KSigma

- [Yahoo 大规模时列数据异常检测技术及其高性能可伸缩架构](https://www.infoq.cn/article/automated-time-series-anomaly-detection/)
- [EGADS介绍(一)--框架处理流程分析](https://www.cnblogs.com/ljhbjehp/p/14287917.html)
- [EGADS介绍(二)--时序模型和异常检测模型算法的核心思想](https://www.cnblogs.com/ljhbjehp/p/14386425.html)
- [yahoo dataset](https://webscope.sandbox.yahoo.com/catalog.php?datatype=s&did=70&guccounter=1)  
## 异常检测

### 场景

1. 金融欺诈检测：通过对多种金融数据指标（如交易金额、交易时间、地理位置、账户余额等）进行分析，检测潜在的欺诈交易。检测逻辑包括比较当前交易数据与历史数据的差异，以及识别异常模式。
2. 工业设备故障检测：对工业设备的多个指标（如温度、压力、振动等）进行监测，检测设备的异常状态以及可能的故障。检测逻辑包括识别异常模式、判断设备是否处于工作状态、以及与其他设备进行比较分析。
3. 网络入侵检测：通过对网络流量的多个指标（如数据包大小、流量类型、来源IP地址等）进行分析，检测潜在的入侵行为。检测逻辑包括识别异常流量模式、建立规则进行匹配、以及分析用户行为。
4. 医疗异常检测：对医疗数据的多个指标（如生命体征、病历、药物使用等）进行监测，检测患者的异常状态以及可能的疾病风险。检测逻辑包括建立基准值、识别异常模式、以及与其他患者进行比较分析。
5. 基础设施监测：对城市基础设施（如道路、桥梁、水电站等）的多个指标（如结构安全、温度、水位等）进行监测，检测潜在的故障风险。检测逻辑包括识别异常模式、建立结构模型进行分析、以及与其他设施进行比较分析。
6. 人脸识别异常检测：对人脸图像的多个指标（如表情、姿态、光线等）进行监测，检测潜在的欺诈或伪造行为。检测逻辑包括建立基准值、识别异常模式、以及与其他人脸进行比较分析。
7. 能源消耗异常检测：对建筑或工业设施的多个指标（如温度、湿度、能源消耗等）进行监测，检测潜在的能源浪费或异常消耗。检测逻辑包括建立基准值、识别异常模式、以及与其他设施进行比较分析。
8. 交通异常检测：对交通数据的多个指标（如车辆速度、密度、车流量等）进行监测，检测交通拥堵、事故或其他异常情况。检测逻辑包括建立基准值、识别异常模式、以及与其他交通情况进行比较分析。
9. 社交媒体异常检测：对社交媒体数据的多个指标（如用户行为、话题、内容等）进行监测，检测虚假信息、舆情危机或其他异常情况。检测逻辑包括建立基准值、识别异常模式、以及与其他社交媒体情况进行比较分析。
10. 农业异常检测：对农业数据的多个指标（如土壤含水量、气象数据、农作物生长情况等）进行监测，检测潜在的病虫害、自然灾害或其他异常情况。检测逻辑包括建立基准值、识别异常模式、以及与其他农业情况进行比较分析。

                 --- ChatGPT

## REF

- [异常检测-综述](https://zhuanlan.zhihu.com/p/260651151) 分类

- [异常检测文章阅读：Deep Weakly-supervised Anomaly Detection(PRO)](https://zhuanlan.zhihu.com/p/431687085) 半监督

- [深度异常检测：Deep SVDD+Deep SAD](https://zhuanlan.zhihu.com/p/447954468)

- [异常检测之SOS算法](https://zhuanlan.zhihu.com/p/34438518) 当一个点和其它所有点的关联度（affinity）都很小的时候，它就是一个异常点

- [GitHub - aws/random-cut-forest-by-aws: An implementation of the Random Cut Forest data structure for sketching streaming data, with support for anomaly detection, density estimation, imputation, and more.](https://github.com/aws/random-cut-forest-by-aws)  java/rust Random Cut Forest (RCF) 算法

#### 业界实践

- [网易游戏AIOps实践：异常检测的优化策略与平台化建设-51CTO.COM](https://www.51cto.com/article/709499.html)
  
  - aiops 能力阶段（无单点应用；单场景运维；串联，流程化，对外服务；无干预，主场景能力完备；中枢，平台）

- [携程实时智能异常检测平台的算法及工程实现_运维_陈剑明_InfoQ精选文章](https://www.infoq.cn/article/sul*elmafxf9tc9zbvwf)
  
  - 目标：
    - 尽力告警，宁可误报，不遗漏。
    - 再对告警压缩，进行人工可处理程度
  - 实时性，Flink
    - 滑动窗口
    - 数据可以基于自身的时间戳来统计，不会因为数据延迟而落到下一个时间窗口来统计
    - 容错
  - java 实现的算法
  - 模型存储 hdfs

- [opendistro ad for es](https://opendistro.github.io/for-elasticsearch-docs/docs/ad/)  产品设计，基于RCF算法

- [基于数据流的异常检测：Robust Random Cut Forest](https://developer.aliyun.com/article/722280)

- [AIOps挑战赛 | 阿里达摩院刘春辰：鲁棒时序异常检测与周期识别](https://www.bizseer.com/index.php?m=content&c=index&a=show&catid=26&id=50)
- [智能运维系列（三）| 浅析智能异常检测：“慧识图”核心算法](https://www.infoq.cn/article/mryjNLXOlujV7fkQFUaL)

“微众银行智能监控系统识图模块”是针对业务四大黄金指标而设计的智能曲线异常检测系统。四大黄金指标包括交易量(业务实时产生的交易量)、业务成功率(业务成功量/交易量)、系统成功率(系统成功量/交易量, 业务成功量和系统成功量的区别在于是否明确捕捉到系统异常)、平均时延(交易的平均耗时)。
(对业务时序数据的异常检测)
识图的检测方法主要有三种：
● 基于 LSTM 与高斯分布的检测，这个算法主要用于交易量和时延的检测。大部分的曲线突变都能准确检测到，但算法的死角在于小幅度长时间的缓慢变化容易被漏掉。
● 基于 k-means 算法的特征检测，主要用于填补第一种算法的盲区,在交易量缓慢变化的案例效果较好。
● 基于概率密度的检测，主要用于业务成功率和系统成功率的曲线，因为成功率曲线的背后隐藏着无数的可能，需要用一个更接近本质的量来衡量异常的程度。

- [大规模Aiops系统在核心网数据中心的探索与实践-算法架构](https://zhuanlan.zhihu.com/p/466955597)
- [基于数据流的异常检测：Robust Random Cut Forest](https://developer.aliyun.com/article/722280)
- [智能运维 | 异常检测：百度是这样做的](https://mp.weixin.qq.com/s?__biz=MzA5NTQ5MzE5OQ==&mid=2653057356&idx=1&sn=85d82226c7f66685ec8cf486569976dc)










### 领域知识

KDDCPU99

#### 基于网络层的攻击行为

- DOS（denial-of-service）  
  拒绝服务攻击，例如 ping-of-death, syn flood, smurf 等
- R2L（unauthorized access from a remote machine to a local machine）  
  来自远程主机的未授权访问，例如 guessing password
- U2R（unauthorized access to local superuser privileges by a local unpivileged user）  
  未授权的本地超级用户特权访问，例如 buffer overflow attacks。
- PROBING（surveillance and probing）  
  端口监视或扫描，例如 ipsweep、 mscan、nmap、portsweep、saint、satan 等

#### [DDOS](https://www.cloudflare.com/zh-cn/learning/ddos/what-is-a-ddos-attack/) 拒绝服务攻击

- HTTP 洪水攻击类似于同时在大量不同计算机的 Web 浏览器中一次又一次地按下刷新 ——大量 HTTP 请求涌向服务器，导致拒绝服务。

- **SYN洪水**（syn flood, 也有名称叫neptune），利用TCP握手链接，通过向目标发送大量伪造源IP的初始连接请求”SYN 数据包来实现。目标计算机响应每个连接请求，然后等待握手中的最后一步，但这一步确永远不会发生，因此在此过程中耗尽目标的资源。

- DNS 放大，利用伪造的 IP 地址（受害者的 IP 地址）向开放式 DNS 服务器发出请求后，目标 IP 地址将收到服务器发回的响应。

- [Ping_of_death](https://en.wikipedia.org/wiki/Ping_of_death) 向计算机发送格式错误或其他恶意的 ping

- [ping flooding](https://en.wikipedia.org/wiki/Ping_flood)

- [Smurf attack - Wikipedia](https://en.wikipedia.org/wiki/Smurf_attack)

- Smurf 攻击是一种分布式拒绝服务攻击，其中使用 IP 广播地址向计算机网络广播大量具有预期受害者的欺骗源 IP 的 Internet 控制消息协议 (ICMP) 数据包。 默认情况下，网络上的大多数设备都会通过向源 IP 地址发送回复来对此做出响应。如果网络上接收和响应这些数据包的机器数量非常多，受害者的计算机就会被流量淹没。这会使受害者的计算机变慢，以至于无法继续工作。

#### [DDOS](https://www.cloudflare.com/zh-cn/learning/ddos/what-is-a-ddos-attack/) 拒绝服务攻击

- HTTP 洪水攻击类似于同时在大量不同计算机的 Web 浏览器中一次又一次地按下刷新 ——大量 HTTP 请求涌向服务器，导致拒绝服务。

- **SYN洪水**（syn flood, 也有名称叫neptune），利用TCP握手链接，通过向目标发送大量伪造源IP的初始连接请求”SYN 数据包来实现。目标计算机响应每个连接请求，然后等待握手中的最后一步，但这一步确永远不会发生，因此在此过程中耗尽目标的资源。

- DNS 放大，利用伪造的 IP 地址（受害者的 IP 地址）向开放式 DNS 服务器发出请求后，目标 IP 地址将收到服务器发回的响应。

- [Ping_of_death](https://en.wikipedia.org/wiki/Ping_of_death) 向计算机发送格式错误或其他恶意的 ping

- [ping flooding](https://en.wikipedia.org/wiki/Ping_flood)

- [Smurf attack - Wikipedia](https://en.wikipedia.org/wiki/Smurf_attack)

- Smurf 攻击是一种分布式拒绝服务攻击，其中使用 IP 广播地址向计算机网络广播大量具有预期受害者的欺骗源 IP 的 Internet 控制消息协议 (ICMP) 数据包。 默认情况下，网络上的大多数设备都会通过向源 IP 地址发送回复来对此做出响应。如果网络上接收和响应这些数据包的机器数量非常多，受害者的计算机就会被流量淹没。这会使受害者的计算机变慢，以至于无法继续工作。

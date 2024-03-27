

## aiops 概览

1) 行业领域知识：应用的行业，如互联网、金融、电信、物流、能源电力、工业制造和智慧城市等，并熟悉生产实践中的难题；
2) 运维场景领域知识：如指标监控、异常检测、故障发现、故障止损、成本优化、容量规划和性能优化等；
3) 机器学习：把实际问题转化为算法问题，常用算法包括如聚类、决策树、卷积神经网络等。


### 数据

管理和分析的数据
- tracing, logging, metric 可观测数据
- alert 告警事件等监控事件数据
- cmdb 元数据
  - 资产信息：包括硬件资产（如服务器、网络设备、存储设备等）和软件资产（如操作系统、应用程序等）的详细信息，例如制造商、型号、序列号、配置等。
  - 关系拓扑：描述IT基础设施中各个配置项之间的关系，例如网络拓扑、系统依赖关系等。
  - 配置项状态：记录配置项的当前状态，包括已部署的软件版本、硬件配置、运行状态等。
  - 变更历史：记录配置项的变更历史，包括变更日期、变更类型、执行人等信息。

### ops流程
- 提前发现风险
  - 容量预测, 运行风险感知, 日志特征,预测未来是否可能故障
- 事件发生时及时发现
  - 异常检测, 告警降噪
- 发现时根因定位
  - 业务影响分析, 异常机器定位, 调用链, 根因分析


## 故障管理

- 阿里云 [AIOps智能故障管理在阿里巴巴集团 的成功实践](https://developer.aliyun.com/article/1088599)
  - 时间序列异常检测 （时序分解的组合算法）
  - 智能根因推荐，故障自动分析及定位
- https://help.aliyun.com/zh/sls/user-guide/overview-1  告警管理系统
- https://developer.aliyun.com/article/1368113 
- https://zhuanlan.zhihu.com/p/664609196 


## OpenAiops
- [课程](), [Advanced Network Management (AIOps) - 裴丹](https://netman.aiops.org/courses/advanced-network-management-spring2023-syllabus/) 论文,材料


## LLM for ops

- [AI大模型运维开发探索第三篇：深入浅出运维智能体](https://mp.weixin.qq.com/s/VNxnatwTpl9srHszyNACXQ)
  - 基于agent 诊断 hdfs 问题
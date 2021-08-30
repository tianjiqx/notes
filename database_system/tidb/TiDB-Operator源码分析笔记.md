# TiDB-Operator源码分析笔记

## 1. 源码结构

版本（2021.08.30）：

`19d98f4c3608a257ea234312c650b76ee2d55f25`

- docs
  - 设计文档、API资源说明文档
- charts
  - Helm charts 文件模板
    - 用于部署TiDB Operator，TiDB Cluster，Backup等应用
- images
  - tidb-operator，backup 镜像构建文件
- deploy
  - 阿里云，aws，谷歌云环境部署的Terraform脚本
- marketplace
  - gcp 谷歌云 环境安装  charts
- manifests
  - yaml 文件，crd 定义
- example
  - tidb on k8s的一些yaml部署 demo脚本，可以用来测试tidb-Operator
- hack
  - e2e 测试 (端到端测试，模仿模仿用户，检查操作链)
- ci
  - 持续集成测试相关脚本
- test
  - 集成测试等，images
- misc
  - 工具集image，debug 、control
- cmd
  - 各组件、工具mian入口
- pkg
  - 主要的源码目录（稍奇怪为什么不是src目录下）



## 2. 功能模块

### 2.1 controller-manager

其参考了kube-controller-manager 的设计。

入口：`cmd/controller-manager/main.go `

- `main()`
  - 读取配置，环境变量
  - 创建与K8S api server连接的客户端`kubeCli`
  - `onStarted`启动逻辑
    - 创建各个Controller，每个控制器单独一个go线程启动，处理事件
    - Controller中的informer用来和 kube-apiserver 交互获取 CRD 和相关资源的变更。
      - 具有处理添加，更新，删除事件的 EventHandler
    - `pkg/controller/tidbcluster/tidb_cluster_controller.go` 集群控制器
      - `func (c *Controller) Run(workers int, stopCh <-chan struct{})` Controller 启动worker
        - `func (c *Controller) processNextWorkItem() bool ` worker死循环处理队列中的事件
          - `func (c *Controller) sync(key string) error `  根据key获取CR对象，并进行状态同步（使集群达到期望的状态）
            - `func (c *Controller) syncTidbCluster(tc *v1alpha1.TidbCluster) `
              - `pkg/controller/tidbcluster/tidb_cluster_control.go` 代码
                - `func (c *defaultTidbClusterControl) UpdateTidbCluster(tc *v1alpha1.TidbCluster) error `  各组件（PD，tikv，tiflash等的Sync）
  - `onStopped` 停止逻辑
  - 为prometheus创建HTTPServer服务
    - 提供metrics

TiDBCluster Controller 负责了 TiDB 主要组件的生命周期管理，TiDB 各个组件的 Member Manager 封装了对应具体的生命周期管理逻辑。

组件控制循环

- TiDB组件
  - `pkg/manager/member`
- Kubernetes 资源管理组件
  - `pkg/manager/meta`



组件生命周期管理：

- 同步 Service；
- 进入 StatefulSet 同步过程；
  - 主要逻辑
- 同步 Status；
- 同步 ConfigMap；
- 处理滚动更新；
- 处理扩容与缩容；
- 处理故障转移；
- 最终完成 StatefulSet 同步过程。



### 2.2 CRD



### 2.3 Scheduler



## 3. 设计思想

TiDB Operator 核心构成：

- CRD
- 自定义控制器
  - 包含业务状态（PD等）+ K8S API状态
- 自定义调度器

好处：

- 基于控制循环的自运维模式

- 基于 Kubernetes 的 Restful API 提供了一套标准的集群管理 API，把 TiDB 集成到用户的工具链、PasS平台。

最佳实践：

在 Kubernetes 上管理有状态应用

- 基于StatefulSet，而非Pod管理。（一般应用推荐的应用部署也是这样吧）

（为 PD、TiKV、TiDB 创建一个 StatefulSet，TiDB计算节点也是StatefulSet，是因为需要存储较大的中间结果）

- 使用Local PV，保证性能，而非网络存储（多副本）
  - 问题：Pod与特定节点绑定，节点故障
  - 解决：应用层多副本（TiDB本身多分布），在正常节点创建新Pod总故障转移，应用的副本数据调度。
  - 实现：
    - 检测：PD与API Server都认为Pod挂掉，才是真正挂掉
      - 避免单边网络问题
    - StatefulSet 副本数加1，进行故障转移，PD与API Server发现节点恢复正常后（现在会多了一些副本数），提示用户删除failure 记录
      - 避免节点迁移频繁
      - 缩容时间，交给用户决策

- 调度
  - 目标：不在一台机器上部署超过半数的 PD 节点（2-2-1 合理）
  - inter-pod anti-affinity 无法实现需求
    - hard 完全禁止2的出现（2-2-1）
    - soft 允许(2-2-1) ，在节点挂掉后转移pod，但是在节点恢复过来之后，不会转移pod，恢复成(2-2-1)
  - 解决：通过调度结果filter机制，过滤实例节点的pod数大于一半的情况
    - 似乎是经过多次调度，filter，然后满足最终的目标拓扑





## REF

- [tidb-operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable)
- [TiDB Operator 源码阅读 (一) 序](https://pingcap.com/zh/blog/tidb-operator-source-code-1)
- [TiDB Operator 源码阅读 (二) Operator 模式](https://pingcap.com/zh/blog/tidb-operator-source-code-2)
- [TiDB Operator 源码阅读 (三) 编排组件控制循环](https://pingcap.com/zh/blog/tidb-operator-source-code-3)
- [TiDB Operator 源码阅读 (四) 组件的控制循环](https://pingcap.com/zh/blog/tidb-operator-source-code-4)
- [文稿分享记录：TiDB Operator 设计与实现](https://zhuanlan.zhihu.com/p/74897388)
- [TiDB on Kubernetes 最佳实践](https://zhuanlan.zhihu.com/p/243134655)



相关链接

- [存算分离/DB on K8s 论文/blog收集](https://zhuanlan.zhihu.com/p/377755864)


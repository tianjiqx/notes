# Kubernetes-笔记

[toc]

## 1. 背景

定义：

**Kubernetes是用于自动部署，扩展和管理容器化应用程序的开源系统。**（生产级别的容器编排系统）

起源于google的Borg系统，在社区的参与（创意和实践）下发展壮大。

面向的问题：

- 现代的 Web 服务，用户希望应用程序能够 24/7 全天候使用
- 开发人员希望每天可以多次发布部署新版本的应用程序

容器化改进了这些问题，但是大规模的容器集群运维成为难题，k8s即用来管理容器集群的工具。



针对大规模尺度（星际尺度）

- google每周运行数十亿个容器，在运维团队不扩展情况下，扩展系统的规模。

特性：

- 自动化上线和回滚
  - 对于应用或配置的更改，分步骤的上线，不会停机所有的实例。
  - 出现问题，回滚所做更改。
- 服务发现和负载均衡
  - 应用程序无需修改，即可使用陌生服务
  - k8s为容器提供ip和dns名称，并使各个容器的负载均衡
    - 自动的负载均衡，可选，应用组件绑定部署，实际有时便于跟踪分析问题。
- 存储编排
  - 自动挂载所选存储系统
    - 本地存储
      - 磁盘
    - 公有云提供商所提供的存储
      - AWS
    - 网络存储系统
      - NFS，Ceph
- 自动装箱
  - 根据资源需求（CPU，RAM）和其他约束自动放置容器，同时避免影响可用性。
  - 高资源需求和低资源需求混合部署，提供资源利用率。
- 水平扩缩
  - 提供命令，UI，或者基于CPU负载自动地对程序进行扩缩
- 自我修复
  - 重新启动失败的容器，自动重试
  - 在节点死亡时替换并重新调度容器
  - 杀死不响应用户定义的健康检查的容器
  - 在容器状态未准备好时，不暴露给客户端
- 秘钥和配置管理
  - Kubernetes允许你存储和管理敏感信息，例如密码、OAuth 令牌和 ssh 密钥。
  - 可以在不重建容器镜像的情况下部署和更新密钥和应用程序配置，
  - 也无需在堆栈配置中暴露密钥。
- 批量执行
  - 支持定义Jobs，批量执行
- ipv4/ipv6支持
  - 为 Pod 和 Service 分配 IPv4 和 IPv6 地址



服务部署的发展：

物理机部署->虚拟化部署（虚拟机VM）-> 容器化部署（应用共享操作系统，但是有独立的文件系统、CPU、内存、进程空间）

容器化优势：

> - 敏捷应用程序的创建和部署：与使用 VM 镜像相比，提高了容器镜像创建的简便性和效率。
> - 持续开发、集成和部署：通过快速简单的回滚（由于镜像不可变性），支持可靠且频繁的容器镜像构建和部署。
> - 关注开发与运维的分离：在构建/发布时而不是在部署时创建应用程序容器镜像， 从而将应用程序与基础架构分离。
> - 可观察性：不仅可以显示操作系统级别的信息和指标，还可以显示应用程序的运行状况和其他指标信号。
> - 跨开发、测试和生产的环境一致性：在便携式计算机上与在云中相同地运行。
> - 跨云和操作系统发行版本的可移植性：可在 Ubuntu、RHEL、CoreOS、本地、 Google Kubernetes Engine 和其他任何地方运行。
> - 以应用程序为中心的管理：提高抽象级别，从在虚拟硬件上运行 OS 到使用逻辑资源在 OS 上运行应用程序。
> - 松散耦合、分布式、弹性、解放的微服务：应用程序被分解成较小的独立部分， 并且可以动态部署和管理 - 而不是在一台大型单机上整体运行。
> - 资源隔离：可预测的应用程序性能。
> - 资源利用：高效率和高密度。（无VM中间开销）

**关于编排：**

Kubernetes非传统意义上的编排系统，实际上它消除了编排的需要。

传统编排：执行A，再执行B，再执行C。

Kubernetes 包含一组独立的、可组合的控制过程， 这些过程连续地将当前状态驱动到所提供的所需状态。 



**关于DevOps、无运维:**

K8S对硬件做抽象，将自身暴露为平台，用于部署和运行应用程序。

**“Kubernetes is the new Linux”**





## 2.架构

### 2.1 架构

![](k8s笔记图片/components-of-kubernetes.svg)

Kubernetes集群：由一组被称作**节点**的机器（可以是虚拟机）组成。

节点：管理节点，工作节点。

工作节点：运行Kubernetes 所管理的容器化应用。（至少一个工作节点）。

应用以**Pod**形式部署,一个应用可以拆分成多个Pod，一个Pod代表一组（1+个）容器，通过指定Pod的副本数，进行横向扩展。

**K8S的架构：**

主从结构。

- 包含一系列组件的控制平面(控制面板)Control Plane（master）
  - 用于管理集群的工作节点和Pod
    - 调度，检查和响应集群事件
  - 组件可以运行在单个master节点，也可以复制，以支持高可用的集群部署
    - 支持自托管
      - 运行在K8S集群本身上
  - 管理节点
    - 一般为了避免业务应用的负载影响，不再作为工作节点
- 节点代理kubelet（主要的节点组件）（slave）
  - 工作节点

**控制平面Control Plane：**

- **kube-apiserver** API服务器
  - 负责提供 HTTP API，以供用户、集群中的不同部分和集群外部组件相互通信。
    - 用户请求及其他系统组件与集群交互的**唯一入口**
  - 查询和操纵 Kubernetes API 中对象（例如：Pod、Namespace、ConfigMap 和 Event）的状态。
    - 提供etcd的封装接口API
    - 集群访问控制
      - 客户端身份验证（Authentication）和授权（Authorization）
      - 资源准入控制（Admission Control）
  - 无状态，可横向扩展
    - 通过Haproxy或负载均衡器 进行协同工作（负载均衡器也可以配置使用多个，避免单点故障）
    
      ![](k8s笔记图片/Snipaste_2021-08-12_20-54-39.png)
- etcd

  - etcd 是兼具一致性和高可用性的键值数据库
  - 保存 Kubernetes 所有集群数据（状态）
    - Node、Service、Pod 的状态和元数据，以及配置数据等
- **kube-scheduler**
  - 监视新创建的、未指定运行节点的Pods（用户要求运行的一组容器），选择节点让Pod在上面运行
  - 调度Pod的过程
    - 调度周期，选择最优节点
    - 绑定周期，通知API Server
- **kube-controller-manager** (cm)
  
  - 统一管理各个控制器的进程
    - 各控制器完成故障检测、自动扩展、滚动更新等功能；
  - 控制器
    - 节点控制器（Node Controller）: 负责在节点出现故障时进行通知和响应
    - 任务控制器（Job controller）: 监测代表一次性任务的 Job 对象，然后创建 Pods 来运行这些任务直至完成
    - 端点控制器（Endpoints Controller）: 填充端点(Endpoints)对象(即加入 Service 与 Pod)
    - 服务帐户和令牌控制器（Service Account & Token Controllers）: 为新的命名空间创建默认帐户和 API 访问令牌
- cloud-controller-manager（ccm）
  - 云平台交互控制器管理
  - 控制器
    - 节点控制器（Node Controller）: 用于在节点终止响应后检查云提供商以确定节点是否已被删除
    - 路由控制器（Route Controller）: 用于在底层云基础架构中设置路由
    - 服务控制器（Service Controller）: 用于创建、更新和删除云提供商负载均衡器

**节点代理组件：**

- **kubelet**

  - 节点的代理，负责维护容器的生命周期，同时也负责 Volume（CSI）和网络（CNI）的管理
  - 容器执行层，Pod和Node API的主要实现者
    - 接收PodSpecs，确保这些PodSpecs中描述的容器处于运行状态且健康。
    - 负责启动容器的守护进程
      - 启动时，向API Server 处创建一个Node 对象来注册自身的节点信息
- kube-proxy
  - 网络代理
  - 为Service 提供 cluster 内部的服务发现和负载均衡
  - DNS查找服务，服务使用静态IP，保证即使容器被迁移，客户端依然能够连接到容器服务。
    - 负载均衡，宕机等情况导致迁移
- Container Runtime
  - 负责运行容器，镜像管理。
  - 支持
    - docker
    - containerd
    - DRI-O
    - 实现Kubernetes CRI 容器运行环境接口的

其他架构图：

![](k8s笔记图片/Snipaste_2021-08-12_17-21-31.png)

![](k8s笔记图片/Snipaste_2021-08-12_21-37-57.png)

![](k8s笔记图片/kubernetes-high-level-component-archtecture.jpg)



### 2.2 概念

#### 2.2.1 容器技术

**基于linux容器技术的组件隔离原理**：

- linux名字空间（namespace）
  - 多种名字空间类型，每种隔离一组特定的资源
    - Mount(mnt)
    - Process ID(pid)
    - Network(net)
    - Inter-process communicaion(ipd)
    - UTS
    - User ID(user)
  - 用于隔离进程
    - 进程只能看到同一个命名空间下的资源
- linux控制组cgroups
  - 用于限制进程的可用资源（CPU，内存，网络带宽等）
    - CPU
      - 限制cpu使用时间
        - cpu.shares、cpu.cfs_period_us 和cpu.cfs_quota_us
    - blkio
      - 对块设备访问控制I/O



**docker 容器平台：**

Docker是一个打包、分发和运行应用程序的平台。

打包应用的库和依赖，打包整个操作系统的文件系统。

使容器能在不同机器之 间移植的系统。

- 镜像images
  - 打包的应用程序及其所依赖的环境
    - 文件系统，元数据（可执行文件路径）
  - 可共享镜像层，但是只读
  - 镜像层之上的可写层，写拷贝

- 镜像仓库Registries
  - 共享镜像

- 容器Containers
  - 基于镜像创建的进程，只能访问和使用分配给它的资源

![](k8s笔记图片/Snipaste_2021-08-12_17-04-21.png)

容器技术的优势：

- 解决不同应用对环境的需求（操作系统，依赖库、各个版本）

![](k8s笔记图片/Snipaste_2021-08-12_17-06-14.png)

#### 2.2.2 Pod

Pod是代表一组并置的容器（也可以是单个容器）。

一个Pod的容器，都运行在同一个节点上。

一个容器一个进程的最佳实践。（进程崩溃，自动重启，记录错误，都是单进程更好处理。）

Pod也可以被当做是多进程的容器，同时运行一些密切相关的进程，提供（几乎）完全相同的环境，又保持一定的隔离性。

- 共享network，UTS名字空间（PID）,存储卷volumne
  - 相同的IP，端口空间
- 隔离的文件系统

Pod是K8S中的基本构建模块。

Pod视为独立的机器。

Pod之间共享IP地址空间（无NAT），通过ip地址相互通信。

专用的网络实现，基于真实链路。（与实际网络拓扑无关）

应用的Pod的设计实践：分层的应用，每层使用一个Pod。（例如Web服务Pod，数据库服务Pod）

（Pod的代价很低，分割到多个Pod中，便于扩缩）



#### 2.3 Volumne

Volume（存储卷） 是Pod中能够被多个容器访问的共享目录。  

支持多种类型的Volume， 例如GlusterFS、 Ceph等先进的分布式文件系统 。



#### 2.4 Kubectl

命令行工具，用于与 Kubernetes 集群和其中的 pod 通信。

- 查看集群的状态
- 列出所有pod
- 进入pod
- 添加使用yaml文件定义资源对象到集群



#### 2.5 Ingress & Egress

进入 Kubernetes pod 的流量称为 Ingress，而从 pod 到集群外的出站流量称为 egress。



#### 2.6 Replica & ReplicaSet

Pod的副本，被称为 Replica。

ReplicationController 或 ReplicaSet 会监控和保证活动副本的数量。

RC是Kubernetes 较早期的技术概念，只适用于长期服务型的业务类型。

RS是新并版本的RC。



#### 2.7 Deployment

表示用户对 Kubernetes 集群的一次更新操作。

范围更大的API 对象，应用级别。

初始：

- 默认命名空间 default 

- 系统命名空间 kube-system



#### 2.8 Namespace

虚拟的隔离Pod。操作管理，显示。



#### 2.9 服务网格Service Mesh

用于管理服务之间的网络流量，云原生的网络基础设施层。




## 3.部署应用

### 3.1 在Kubernetes中运行应用  

- 将应用打包进一个或多个容器镜像
- 镜像推送到镜像仓库
- 将应用的描述发布到 Kubemetes API 服务器
  - 描述
    - 容器（组件）镜像，应用组件关联
    - 哪些组件需要同时运行在同一个节点上和哪些组件不需要同时运行
    - 哪个暴露IP地址，对外提供服务的组件
-  Kubemetes API 服务器根据描述，创建Pods
- 调度器kube-scheduler，调度pod到可用的工作节点上
  - 基于每组需要的资源、节点存在的未分配的资源
- 工作节点上的Kubelet 将从镜像仓库拉取镜像并运行容器

![](k8s笔记图片/Snipaste_2021-08-12_17-42-52.png)



三组pod，pod的数字是副本数，pod可以包含多个容器。



## 4.组件详细





**Pod创建流程：**

![](k8s笔记图片/Snipaste_2021-08-12_21-04-58.png)





## 5.设计哲学

### 5.1 对象的通用设计原则

API：

- Kubernetes 将业务模型化，这些对象的操作都以API 的形式发布出来
  - 因此其所有API 设计都是声明式的
- 所有API对象应该是互补和可组合的
  - 通过组合关系构建的系统
  - 不封装API，提供泛操作
- 高层 API 以操作意图为基础设计
  - K8S业务需求（调度管理容器的操作）出发
- API 操作复杂度应该与对象数量成线性或接近线性比例
  - 系统的规模扩展性
- API 对象状态不能依赖于网络连接状态
- 尽量避免让操作机制依赖于全局状态
- API 对象的内部表示与任何一个 API 版本分离
  - 内部结构能够表达所有版本化API对象
    - 前向、后向兼容

[API 变更](https://git.k8s.io/community/contributors/devel/sig-architecture/api_changes.md#readme)、[API 废弃策略](https://kubernetes.io/zh/docs/reference/using-api/deprecation-policy/)

控制器：

- 控制器的行为应该是可重入和幂等
  - 通过幂等的控制器使得系统一致朝用户期望状态努力，且结果稳定
- 控制逻辑应该只依赖于当前状态
- 假设任何错误的可能，并做容错处理
- 模块在出错后，可以自动恢复



### 5.2 声明式设计Declarative  

一种软件设计理念和做法：

我们向一个工具描述我们想要让一个事物达到的目标状态，由这个工具自己内部去figure out如何令这个事物达到目标状态。

典型：SQL、YAML

在 Kubernetes 中，使用YAML文件定义对象，服务的拓扑结构、状态。



好处：

- 简单，使用者无需关心过程细节。
- 自我描述的文档



相对比的是过程式、命令式，描述动作。



### 5.3 分层架构

![](k8s笔记图片/arch-roadmap-1.png)

- 核心层：Kubernetes 最核心的功能，对外提供 API 构建高层的应用，对内提供插件式应用执行环境
  - 容器运行时接口CRI
  - 容器网络接口CNI
  - 容器存储接口CSI
  - 镜像仓库
  - 云服务
  - 身份服务
- 应用层：部署（无状态应用、有状态应用、批处理任务、集群应用等）和路由（服务发现、DNS 解析等）
- 管理层：系统度量（如基础设施、容器和网络的度量），自动化（如自动扩展、动态 Provision 等）以及策略管理（RBAC、Quota、PSP、NetworkPolicy 等）
- 接口层：kubectl 命令行工具、客户端 SDK 以及集群联邦
- 生态系统：在接口层之上的庞大容器集群管理调度的生态系统，可以划分为两个范畴
  - Kubernetes 外部：日志、监控、配置管理、CI、CD、Workflow、FaaS、OTS 应用、ChatOps 等
  - Kubernetes 内部：CRI、CNI、CVI、镜像仓库、Cloud Provider、集群自身的配置和管理等



### 5.4 模型设计



### 5.5 控制器模式







### 5.6 高可用

- 自身组件，依赖etcd 服务解决高可用问题。
- Pod
  - 数据、配置与容器分离，定期检查Pod状态，重启故障Pod
- Node
  - Pod 分散部署在各个工作Node上
- Cluster
  - Federation 机制







## REF

- [kubernetes 官网](https://kubernetes.io/)
- [K8S 官方中文文档](https://kubernetes.io/zh/docs/concepts/)
- [github 社区](https://github.com/kubernetes/community.git) 架构、设计方案
- [Kubernetes生产化实践之路-孟凡杰](https://weread.qq.com/web/reader/cbe32c6072226556cbea464kc81322c012c81e728d9d180) 2020
- Kubernetes in Action
- Kubernetes进阶实战（第2版）-马永亮-2021
- [CloudNative学习笔记](https://github.com/skyao/learning-cloudnative)
- Kubernetes权威指南 第4版
- [Kubernetes Handbook——Kubernetes 中文指南/云原生应用架构实践手册](https://jimmysong.io/kubernetes-handbook/)
- [Istio 服务网格](https://jimmysong.io/istio-handbook/)
- Kubernetes源码剖析-郑东旭-2020


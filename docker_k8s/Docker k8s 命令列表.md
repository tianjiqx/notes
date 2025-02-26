## Docker & k8s 命令列表

[TOC]

### 1.Docker

```shell
docker ps // 列出当前运行的容器 
docker logs // 展示容器的标准的输出（比如hello world） 
docker stop // 停止正在运行的容器 
docker version //可以查看守护的进程，docker版本以及go版本（docker本身是用go语言写的） 
//总结，可以看出docker的命令一般为 [sudo] docker [subcommand] [flags] [arguments] 


// 列出所有创建的容器ID 
docker ps -a -q 
// 删除容器 docker rm xxx 
// 查看镜像 docker images 
// 退出容器但不关闭 ctrl+p+q 
// 退出容器且关闭 ctrl+d

// 进入容器
sudo docker exec -it 775c7c9ee1e1 /bin/bash 

// 暴露特定端口到主机的特定端口
docker run -p 80:80
// 暴露容器的所有端口（exposed 端口）到主机的随机端口
docker run -P
// 查看容器暴露的端口
docker port CONTAINER [PRIVATE_PORT[/PROTO]]

===============
查看已退出容器的log
docker inspect 9dc9349df220 | grep log

//查看容器退出原因
docker inspect 9dc9349df220 | grep -A15 State

//查看容器的信息 image id
docker inspect 0fc0ce8eded4（容器id） 

构建镜像，本地Dockerfile
docker build -t tx-node7:5000/transwarp/inceptor:serdeperformance429 .

// 基于容器构建镜像
docker commit <container_id> <image_name>:<image_tag>

// 获取构建信息
docker history --format {{.CreatedBy}} --no-trunc=true <imagesid>

// 保存镜像
docker save -o myimage.tar myimage:latest

// 恢复镜像
docker load -i myimage.tar

===============
//拷贝 (文件，目录相同，不需要参数-r)
docker cp 7264139ea7eb:/usr/lib/inceptor/lib/idbc-core-8.1.0.jar idbc-core-8.1.0.jar
kubectl cp message.log mysql-478535978-1dnm2:/tmp/message.log

===============
// 显示空间使用
docker system df
// 回收空间
docker system prune

// 从主机中移除镜像
sudo docker rmi 镜像名称
//删除镜像tag（相同image id有多余tag ）,none tag时，可以先加tag，后删
docker rmi REPOSITORY:TAG


// 删除所有关闭的容器：
docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm
// 删除所有dangling镜像（即无tag的镜像）：
docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
docker rmi $(docker images | grep inceptor | grep "^<none>" | awk "{print $3}")


//删除所有dangling数据卷（即无用的Volume）：
docker volume rm $(docker volume ls -qf dangling=true)

===============
// docker 服务状态
systemctl status docker -l
systemctl status kubelet -l
systemctl status haproxy -l

// 重启服务
systemctl restart docker 
systemctl restart kubelet

docker-compose 启动后，容器间无法ping通，ifconfig检查发现没有docker0， 重启docker服务解决
```

### 2. K8S

```shell
// 查看名字空间
kubectl get namespace

// 查看名字空间下的pod
kubectl get pods --namespace=development
kubectl describe pod podname

// 指定名字空间 , -o wide 获取 ip 、node 等信息 
-n namespace
kubectl -n hde6ti7 get pods  -o wide |grep name

// 删除deployment
kubectl delete deployment xxxx
// 查看服务对应的deployment
kubectl get deployment 

// 查看configmap
kubectl -n keta-jks-qx get configmap 
kubectl -n keta-jks-qx get configmap pandora-config -o yaml
// 编辑
kubectl -n keta-jks-qx edit configmap pandora-config

// 多容器， -c 指定
kubectl -n keta-jks-ml-server exec -it pandora-0 -c pandora bash

=========
// 查看1000行kubelet的日志；
journalctl -u kubelet -n 1000
// 查看100行docker的日志；

journalctl -u docker  -n 100 


// 查看pod信息，为什么启动失败事件
// 查看日志
kubectl logs  <podname>
// -p, --previous[=false]: 如果为true，输出pod中曾经运行过，但目前已终止的容器的日志

// 查看前一次启动报错
kubectl logs -p
// 只打印末尾100行
kubectl logs --tail=100 -f  <podname>

=========
// node信息
kubectl get nodes -o wide

// 打印各个node详细信息（容器的cpu分配，内存限制）
kubectl describe node <node_name>

// 查看当前节点停止容器的状态
docker inspect <退出的容器的id> | grep -A15 State


// 查看 tos 相关pod状态
kubectl -n kube-system get pods -o wide
查看hdfs pod状态
kubectl get pods -o wide | grep hdfs

kubectl get events --sort-by=.metadata.creationTimestamp | grep hdfs
kubectl get events --sort-by=.metadata.creationTimestamp | grep inceptor
```


### `get service` 和 `get pod` 获取的 ip 区别 

`get service` 和 `get pod` 是 Kubernetes 中 `kubectl` 命令行工具的两个不同的子命令，它们用于获取不同类型的信息，并且返回的 IP 地址也有所不同。

- `get service`：
   当你执行 `kubectl get service` 命令时，你会获取到 Kubernetes 服务（Service）的相关信息。服务是 Kubernetes 中的一个抽象层，它定义了如何访问一组 Pod。服务通常有一个稳定的虚拟 IP 地址（ClusterIP），这个 IP 地址不会随着 Pod 的变动而改变。这意味着，无论后端的 Pod 如何变化，服务的 IP 地址都保持不变，从而保证了应用程序的连续性和稳定性。
   - **ClusterIP**：这是服务的内部 IP 地址，它在集群内部使用，以便其他组件可以访问该服务。这个 IP 地址对于集群外部是不可见的。
   - **NodePort** 或 **LoadBalancer**：如果服务配置了 NodePort 或 LoadBalancer 类型，它会有一个与集群节点的 IP 地址或外部负载均衡器的 IP 地址相关联的端口。这个 IP 地址可以从集群外部访问服务。

- `get pod`：
   当你执行 `kubectl get pod -owide` 命令时，你会获取到 Pod 的列表和相关信息。Pod 是 Kubernetes 中的最小部署单元，它是一个或多个容器的集合，运行在同一个网络命名空间中。
   - **Pod IP**：这是分配给每个 Pod 的 IP 地址。这个 IP 地址是动态的，可能会随着 Pod 的创建、销毁或重启而改变。
   - **Node IP**：如果 Pod 是运行在特定节点上的，你也可以看到节点的 IP 地址，但这通常不是通过 `get pod` 命令直接获取的。

总结来说，`get service` 命令返回的是服务的 IP 地址，它提供了一种稳定的访问后端 Pod 的方式，而 `get pod` 命令返回的是 Pod 自身的 IP 地址，这个地址是动态的，可能会变化。服务的 IP 地址（ClusterIP）用于集群内部通信，而 Pod 的 IP 地址通常用于调试和内部组件间的通信。如果你需要从集群外部访问应用程序，你可能需要查看服务的 NodePort 或 LoadBalancer IP 地址。



## blogs:

- [aarch cpu架构下 docker 安装](https://www.cnblogs.com/leozhanggg/p/16660866.html)

## install

- [aliyun docker](https://help.aliyun.com/zh/ecs/use-cases/install-and-use-docker#8dca4cfa3dn0e)

普通用户权限配置：
```
# 将当前用户添加到 docker 组：
sudo usermod -aG docker $USER
# 刷新用户组信息
newgrp docker

```
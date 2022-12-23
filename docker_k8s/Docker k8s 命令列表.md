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
docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm//
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

// 指定名字空间 
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


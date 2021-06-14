## Docker & k8s 命令列表

Todo:refine

### 1.Docker

docker ps // 列出当前运行的容器 

docker logs // 展示容器的标准的输出（比如hello world） 

docker stop // 停止正在运行的容器 

docker version //可以查看守护的进程，docker版本以及go版本（docker本身是用go语言写的） 

//总结，可以看出docker的命令一般为 [sudo] docker [subcommand] [flags] [arguments] 



//﻿列出所有创建的容器ID 

docker ps -a -q 

//﻿删除容器 docker rm xxx 

//查看镜像 docker images 

//退出容器但不关闭 ctrl+p+q 

// 退出容器且关闭 ctrl+d



//进入容器

sudo docker exec -it 775c7c9ee1e1 /bin/bash 



//从主机中移除镜像

sudo docker rmi 镜像名称

//删除镜像tag（相同image id有多余tag ）,none tag时，可以先加tag，后删

docker rmi REPOSITORY:TAG



查看已退出容器的log

docker inspect 9dc9349df220 | grep log



查看容器退出原因

docker inspect 9dc9349df220 | grep -A15 State

查看容器的信息 image id

docker inspect 0fc0ce8eded4（容器id） 

构建镜像，本地Dockerfile

docker build -t tx-node7:5000/transwarp/inceptor:serdeperformance429 .

\#拷贝

docker cp 7264139ea7eb:/usr/lib/inceptor/lib/idbc-core-8.1.0.jar idbc-core-8.1.0.jar

kubectl cp message.log mysql-478535978-1dnm2:/tmp/message.log



显示空间使用

docker system df

回收空间

docker system prune



删除所有关闭的容器：

docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm

删除所有dangling镜像（即无tag的镜像）：

docker rmi $(docker images | grep "^<none>" | awk "{print $3}")

docker rmi $(docker images | grep inceptor | grep "^<none>" | awk "{print $3}")



删除所有dangling数据卷（即无用的Volume）：

docker volume rm $(docker volume ls -qf dangling=true)





-- docker 服务状态

systemctl status docker -l

systemctl status kubelet -l

systemctl status haproxy -l

-- 重启服务

systemctl restart docker 

systemctl restart kubelet



### 2. K8S

#查看名字空间

kubectl get namespace

\#查看名字空间下的pod

kubectl get pods --namespace=development

指定名字空间 

-n namespace

kubectl -n hde6ti7 get pods  -o wide |grep name



\# 查看1000行kubelet的日志；

journalctl -u kubelet -n 1000 

\# 查看100行docker的日志；

journalctl -u docker  -n 100 



查看pod信息，为什么启动失败事件

kubectl describe pod podname



\#删除deployment

\#查看服务对应的deployment

kubectl get deployment 

kubectl delete deployment xxxx



\#查看日志 

kubectl logs  <podname>

\#-p, --previous[=false]: 如果为true，输出pod中曾经运行过，但目前已终止的容器的日志

\#查看前一次启动报错

kubectl logs -p



\#确认node信息

kubectl get nodes -o wide

\#打印各个node详细信息（容器的cpu分配，内存限制）

kubectl describe node <node_name>

\# 查看当前节点停止容器的状态

docker inspect <退出的容器的id> | grep -A15 State



查看 tos 相关pod状态

kubectl -n kube-system get pods -o wide

查看hdfs pod状态

kubectl get pods -o wide | grep hdfs

kubectl get events --sort-by=.metadata.creationTimestamp | grep hdfs

kubectl get events --sort-by=.metadata.creationTimestamp | grep inceptor
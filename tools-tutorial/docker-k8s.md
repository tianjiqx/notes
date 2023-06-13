## Docker

### ========================实用命令=================

- docker version //可以查看守护的进程 

- 查看正在运行的容器 
  
  sudo docker ps -ls 

- 列出所有创建的容器ID 
  
  docker ps -a -q 

- 删除容器 
  
  docker rm xxx 

- 查看镜像
  
  docker images 

- 退出容器但不关闭 
  
  ctrl+p+q 

- 退出容器且关闭 
  
  ctrl+d

- 从主机中移除镜像
  
  sudo docker rmi 镜像名称

- 删除镜像tag（相同image id有多余tag ）
  
  docker rmi REPOSITORY:TAG

- 停止正在运行的container
  
  sudo docker stop containerName

- 移除某个container
  
  sudo docker rm containerID

- 创建Docker用户组，避免使用sudo
  
  //添加一个用户组 
  
  sudo usermod -aG docker you //you是用户组名，一般用你当前电脑的用户 
  
  //将you从docker用户组移除 
  
  sudo gpasswd -d you docker 
  
  //删除刚才创建的docker用户组 
  
  sudo groupdel docker 

- 查看容器的信息 image id
  
  docker inspect 0fc0ce8eded4（容器id） 
  
  docker inspect 0fc0ce8eded4 |grep Image

- 换images，备份原来的docker image
  
  docker tag 原来的image id REPOSITORY:TAG_bak

- 换images，新的镜像的tag和push
  
  docker tag newimage_id REPOSITORY:TAG

- 换images，上传到本地仓库
  
  docker push REPOSITORY:TAG

- 显示空间使用
  
  docker system df

- 回收空间
  
  docker system prune

## K8S

- 查看启动脚本
  
  kubectl describe pod pod_name  #查看pod详细信息

- 查看pods
  
  kubectl get pods
  
  kubectl get pods |grep $keys |awk '{print $1}

- 进入pod并执行命名
  
  kubectl exec -it $podname -- beeline -u jdbc:hive2://localhost:10000

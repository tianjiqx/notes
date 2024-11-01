# Arthas使用

## 1.安装

从 [arthas](https://arthas.aliyun.com/doc/download.html) release 下载。  

```shell
# 下载
curl -O https://alibaba.github.io/arthas/arthas-boot.jar

# 指定用户
sudo -u hive -EH java -jar arthas-boot.jar

# 上传到 k8s 的pod中
kubectl -n pandora-cs-quxing cp arthas-bin.zip pandora-master-0:/usr/share/pandora/arthas-bin.zip

# 进入pod
kubectl -n pandora-cs-quxing exec -it pandora-master-0  bash

# 解压
unzip arthas-bin.zip

# 进入 arthas
java -jar arthas-boot.jar
[INFO] arthas-boot version: 3.5.5
[INFO] Found existing java process, please choose one and input the serial number of the process, eg : 1. Then hit ENTER.
* [1]: 6 org.elasticsearch.bootstrap.Elasticsearch
1

# 指定用户
sudo -u hive -EH java -jar arthas-boot.jar
sudo -u hive  java -jar /home/hive/arthas-boot.jar 
```

## 2. 常用命令

### 2.1 基本

```shell
# 展示当前进程的信息，按ctrl+c可以中断执行。
dashboard
cls——清空当前屏幕区域

# thread 展示线程信息 
thread
# thread 1会打印线程ID 1的栈

# watch 命令, 观察方法的参数和返回值, -x 指定 属性的显示级别层次
watch io.tianjiqx.ClassName methodName  "{params,returnObj}" -x 4

# trace 命令, 查看子调用用时，同时知道在哪一步抛出了异常
trace class-pattern method-pattern

# getstatic 命令获取静态成员值
getstatic 类名 属性名

# jvm相关
dashboard——当前系统的实时数据面板
thread——查看当前 JVM 的线程堆栈信息
jvm——查看当前 JVM 的信息
sysprop——查看和修改JVM的系统属性
sysenv——查看JVM的环境变量
vmoption——查看JVM诊断信息
perfcounter——查看当前 JVM 的Perf Counter信息
logger——查看和修改logger
getstatic——查看类的静态属性

JVM系统属性: 
- 特定于JVM的键值对，可以被在同一JVM实例中运行的所有Java应用程序访问
- System.setProperty() 或者 命令行设置(一般 -D前缀), 常见 -Duser.timezone, -Dfile.encoding, -Xms -Xmx

JVM环境属性:
- 特定于JVM运行的操作系统或执行环境
- export 设置, System.getenv() 获取
# class相关
sc——查看JVM已加载的类信息
sm——查看已加载类的方法信息

# 根据前缀，搜索 
sc io.tianjiqx.ClassPrefix* 
```

### 2.2 火焰图

profiler 之前 允许 
sudo sysctl kernel.perf_event_paranoid=1

```shell
# 生成火焰图：
profiler start  （默认cpu）

# 指定采样事件
--event alloc


profiler start --event wall

$ profiler list
Basic events:
  cpu
  alloc 分析内存
  lock
  wall
  itimer
Perf events:
  page-faults
  context-switches
  cycles
  instructions
  cache-references
  cache-misses
  branches
  branch-misses
  bus-cycles
  L1-dcache-load-misses
  LLC-load-misses
  dTLB-load-misses
  mem:breakpoint
  trace:tracepoint

profiler status

# 停止火焰图
profiler stop --format html 

profiler stop --format html --file /tmp/result.html

# 指定执行时间(s)， -d 10
profiler start --duration 10


# 指定cpu和 wall 时间， 采样间隔 10ms 和 100ms
profiler start -e cpu -i 10 --wall 100 -f out.jfr

生成的结果可以用支持 jfr 格式的工具来查看。比如：

JDK Mission Control ： https://github.com/openjdk/jmc
JProfiler ： https://github.com/alibaba/arthas/issues/1416


```

## 3.问题

### 3.1 K8S 环境生成火焰图报错 “Perf events unavailble. See stderr of the target process”

按[文档](https://my.oschina.net/u/1760791/blog/4773494) 提到的方式，修改pod的deployment配置文件未生效。

后来直接在宿主机环境上，修改`perf_event_paranoid` 配置，成功

```shell
sysctl kernel.perf_event_paranoid=1
# 或者
echo 1 > /proc/sys/kernel/perf_event_paranoid
```

## REF

- [arthas](https://arthas.aliyun.com/doc/download.html)
  - [profiler](https://arthas.aliyun.com/doc/profiler.html)

- [看看我给Arthas官方提供的容器中生成火焰图问题解决方案](https://my.oschina.net/u/1760791/blog/4773494)
- [Arthas使用教程(8大分类)](https://www.cnblogs.com/lydms/p/16549145.html)
- [Arthas 之通过 thread 命令定位线程问题](https://jueee.github.io/2020/08/2020-08-13-Arthas%E4%B9%8B%E9%80%9A%E8%BF%87thread%E5%91%BD%E4%BB%A4%E5%AE%9A%E4%BD%8D%E7%BA%BF%E7%A8%8B%E9%97%AE%E9%A2%98/)
  - 定位 CPU 使用较高的线程
    -  thread -n 5 top5 高使用率线程
  - 定位线程阻塞
    -  thread | grep pool 
  - 定位线程死锁
    - thread -b 
- [Arthas 之定位方法调用问题](https://jueee.github.io/2020/08/2020-08-14-Arthas%E4%B9%8B%E5%AE%9A%E4%BD%8D%E6%96%B9%E6%B3%95%E8%B0%83%E7%94%A8%E9%97%AE%E9%A2%98/)
  - trace 命令 定位耗时问题
    - ``
  - monitor 统计方法耗时
    - `monitor -c 10 sample.demo.controller.UserController getUser`
  - stack 方法调用路径
    - `stack sample.demo.controller.UserController getUser`


## Linux 笔记

### 经验
- [磁盘满了，为啥du却显示还有很大空间？](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961840&idx=1&sn=d3f2600d0c01b926285c244e54be55f0&chksm=bd2d0c2c8a5a853a3bb8465a75878c9c3e25705fd8e1b9a33f60ca621b1bdb012a9609b6f5a)

  学习到的命令：`lsof |grep deleted` 获取已经删除但仍然在被引用的文件，发现后可以尝试杀死进程

- [Linux下查看电脑硬件环境的命令](https://blog.csdn.net/wjlwangluo/article/details/77511692)

- 磁盘命令lsblk，查看分区，逻辑卷物理磁盘位置

- [CPU 信息](https://www.cnblogs.com/charlesblc/p/8309563.html)

  命令1：cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

  命令2：cat /proc/cpuinfo| grep "cpu cores"| uniq # 查看每个物理CPU中core的个数(即核数)

  命令3：cat /proc/cpuinfo| grep "processor"| wc -l

  命令4: cat /proc/meminfo #查看内存信息 free -g

- [判断Linux进程在哪个CPU核运行的方法](https://blog.csdn.net/ibless/article/details/82431101)

  命令1：taskset -c -p <pid>  #找出被固定的CPU内核

  命令2：ps -o pid,psr,comm -p <pid>   #当前分配到的cpu内核

  命令3：top 后按 1 查看cpu各核使用使用比例 

- [分析磁盘i/o---top iostat iotop](https://blog.csdn.net/mao_xiaoxi/article/details/88392955)

  命令1：iostat -x 1 10  # %util接近100%,表明I/O请求太多,I/O系统已经满负荷，磁盘可能存在瓶颈,一般%util大于70%,I/O压力就比较大，读取速度有较多的wait

  命令2: iostat -dx

  命令３：iostat -xmdz 1

  机械硬盘读写速度：5400 r/s 60-90MB 7200 r/s 130-190MB

  ssd: stat2.0 r:225MB/S  w:71MB/S stat3.0 r: 311MB/S

- [ifstat命令_统计网络接口活动状态的工具](https://www.cnblogs.com/friday0502/p/9450562.html)
  
- [使用jstack命令查看CPU高占用的问题记录](https://www.cnblogs.com/xujanus/p/11275413.html)

  命令1：top -Hp <pid>  #高cpu使用进程线程使用情况
  
  命令2：printf "%x\n" thread_id  # 线程号 进行换算成16
  
  命令3：sudo -u hive jstack <pid> |grep "nid=0x十六进制线程号" -A 30  # -A 30 打印后30行，-C 10 打印关键字前后10行

- 使用nmon,sar,dstat分析磁盘、网络IO情况，是否达到瓶颈

- `Dmesg -T` : 检查内核输出信息（OOM kill 等）

- `top -H -p  <pid> ` 查看进程的孩子线程，进程


  ## linux 工具blog 链接
  - [木子的搬砖工具](https://blog.k8s.li/My-brick-lifting-tools.html)

  


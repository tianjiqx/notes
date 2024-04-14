#### Perf-tools-笔记

## 1. Perf-tools

用于 Linux ftrace 和 perf_events（又名“perf”命令）的各种开发中和不受支持的性能分析工具的集合。



## 2.常用分析命令

### 2.1 Cache 分析

#### 2.1.1 Linux 页面缓存的基本缓存命中/未命中统计信息

```shell
sudo ./bin/cachestat -t
USAGE: cachestat [-Dht] [interval]
                 -D              # print debug counters
                 -h              # this usage message
                 -t              # include timestamp
                 interval        # output interval in secs (default 1)
                 
Counting cache functions... Output every 1 seconds.
TIME         HITS   MISSES  DIRTIES    RATIO   BUFFERS_MB   CACHE_MB
14:48:43    34650        0       69   100.0%         3531      49416
14:48:44    32985        0      397   100.0%         3531      49416
14:48:45     1824        0      131   100.0%         3531      49416
```



### 2.2 CPU 分析

#### 2.2.1 perf top

实时查看当前系统进程函数占用率情况

- -g：得到函数的调用关系图
- -e <event>：指明要分析的性能事件
- -p <pid>：Profile events on existing Process ID (comma sperated list). 仅分析目标进程及其创建的线程
- -d <n>：界面的刷新周期，默认为2s，因为perf top默认每2s从mmap的内存区域读取一次性能数据。

```shell
perf top -g -p <pid>

Samples: 182  of event 'cycles:ppp', 4000 Hz, Event count (approx.): 22351023
  Children      Self  Shared Object       Symbol
+   35.89%     2.57%  [kernel]            [k] do_syscall_64
+   28.38%     0.00%  [kernel]            [k] entry_SYSCALL_64_after_hwframe
+   24.91%     0.00%  libpthread-2.28.so  [.] start_thread
+   24.91%     0.00%  libjvm.so           [.] thread_native_entry
+   24.91%     0.00%  libjvm.so           [.] Thread::call_run
+   21.79%     0.29%  libpthread-2.28.so  [.] pthread_cond_timed

# 分析分支预测失败
sudo perf top -e branch-misses -p <pid>
Samples: 505  of event 'branch-misses', 4000 Hz, Event count (approx.): 910661
Overhead  Shared Object       Symbol
  11.96%  libjvm.so           [.] IndexSetIterator::advance_and_next
   3.57%  libjvm.so           [.] PhaseChaitin::gather_lrg_masks
   2.78%  libjvm.so           [.] PhaseChaitin::interfere_with_live
   2.66%  libjvm.so           [.] PhaseChaitin::post_allocate_copy_removal
   2.61%  libjvm.so           [.] PhaseChaitin::elide_copy
   2.14%  libjvm.so           [.] PhaseLive::compute
   1.86%  libjvm.so           [.] PhaseIdealLoop::build_loop_early
   1.37%  libjvm.so           [.] PhaseIdealLoop::build_loop_late_post
   1.31%  libjvm.so           [.] PhaseChaitin::Split
   1.30%  libjvm.so           [.] PhaseChaitin::build_ifg_physical
   1.22%  libjvm.so           [.] find_lowest_bit

```

#### 2.2.2 perf stat

```shell
perf stat [-e <EVENT> | --event=EVENT] [-a] <command>
perf stat [-e <EVENT> | --event=EVENT] [-a] — <command> [<options>

$sudo perf stat
^C
 Performance counter stats for 'system wide':

         403655.94 msec cpu-clock                 #   31.996 CPUs utilized
            118045      context-switches          #    0.292 K/sec
              1753      cpu-migrations            #    0.004 K/sec
             88703      page-faults               #    0.220 K/sec
       32509892817      cycles                    #    0.081 GHz
       23742959822      instructions              #    0.73  insn per cycle
        4911790829      branches                  #   12.168 M/sec
          66660370      branch-misses             #    1.36% of all branches

      12.615713625 seconds time elapsed

cpu-clock：任务真正占用的处理器时间，单位为ms。CPUs utilized = task-clock / time elapsed，CPU的占用率。
context-switches：程序在运行过程中上下文的切换次数。
CPU-migrations：程序在运行过程中发生的处理器迁移次数。Linux为了维持多个处理器的负载均衡，在特定条件下会将某个任务从一个CPU迁移到另一个CPU。
CPU迁移和上下文切换：发生上下文切换不一定会发生CPU迁移，而发生CPU迁移时肯定会发生上下文切换。发生上下文切换有可能只是把上下文从当前CPU中换出，下一次调度器还是将进程安排在这个CPU上执行。
page-faults：缺页异常的次数。当应用程序请求的页面尚未建立、请求的页面不在内存中，或者请求的页面虽然在内存中，但物理地址和虚拟地址的映射关系尚未建立时，都会触发一次缺页异常。另外TLB不命中，页面访问权限不匹配等情况也会触发缺页异常。
cycles：消耗的处理器周期数。如果把被ls使用的cpu cycles看成是一个处理器的，那么它的主频为2.486GHz。可以用cycles / task-clock算出。
stalled-cycles-frontend：指令读取或解码的质量步骤，未能按理想状态发挥并行左右，发生停滞的时钟周期。
stalled-cycles-backend：指令执行步骤，发生停滞的时钟周期。
instructions：执行了多少条指令。IPC为平均每个cpu cycle执行了多少条指令。
branches：遇到的分支指令数。branch-misses是预测错误的分支指令数。
```

### 2.3 Disk 分析

### 2.3.1 跟踪磁盘 I/O 的详细信息，包括延迟



## 3. 可能遇到的问题

### 3.1 K8S 环境使用perf-tools

perf-tools 需要root权限，需要pod 的用户是root，或者Dockerfile创建用户时添加sudo 权限。

[Pod安全上下文](https://kubernetes.io/zh/docs/tasks/configure-pod-container/security-context/) 和[Pod 安全策略](https://kubernetes.io/zh/docs/concepts/policy/pod-security-policy/)中配置。

```
podSecurityContext:
  fsGroup: 1000  # 1000 是创建的用户id
  runAsUser: 1000

securityContext:
	privileged: true #  Processes in privileged containers are essentially equivalent to root on the host.
  capabilities: 
    drop: []

  runAsNonRoot: false
  runAsUser: 1000
```

同时，容器未自动挂载debugfs时，需要手动挂载 `mount -t debugfs debugfs /sys/kernel/debug `

- [mount](https://www.cnblogs.com/sparkdev/p/9015312.html)
- [debugfs](https://www.cnblogs.com/wwang/archive/2011/01/17/1937609.html) [wiki](https://en.wikipedia.org/wiki/Debugfs)

可选，需要perf相关功能时，安装perf

```shell
# 容器系统版本, uname -r 将获取的是物理机的系统版本
cat /etc/issue
Debian GNU/Linux 10 \n \l
# Debian 系统安装命令
sudo apt install linux-perf
# ubuntu 系统
# apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`

# 重命名，由于/usr/bin/perf 脚本中使用uname -r 获取的系统版本不正确
sudo cp /usr/bin/perf_4.19 /usr/bin/perf_5.4
```

将perf-tools 拷贝到容器后即可使用

```shell
kubectl -n <namespace> cp perf-tools <podname>:/usr/share/perf-tools
```



## REF

- [github:perf-tools](https://github.com/brendangregg/perf-tools)
- [slides: Linux Performance Tools](https://www.brendangregg.com/Slides/Velocity2015_LinuxPerfTools.pdf)
- [perf tutorial](https://perf.wiki.kernel.org/index.php/Tutorial#Introduction)
- [perf](https://www.brendangregg.com/perf.html)
- [系统级性能分析工具perf的介绍与使用](https://www.cnblogs.com/arnoldlu/p/6241297.html)
- [linux系统分析之工具大全(观测，性能分析等)](https://zhuanlan.zhihu.com/p/526432016?)





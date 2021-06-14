## 简介
EXSi是VMware公司发布的一种物理机虚拟化产品，可当做一种类linux操作系统，用于管理整个服务器的资源，虚拟化出需要的虚拟机，相对与VMware Workstation 而言减少了操作系统一层，避免了性能损耗。

### 使用工具

- EXSi5.5.0的镜像： VMware-VMvisor-Installer-5.5.0-1331820.x86_64.iso   
- U盘启动盘制作工具：refus
- EXSi5.5 服务器的客户端VMare vSphere Client: VMware-viclient-all-5.5.0-1281650.exe

工具下载地址：
- EXSi5.5: https://pan.baidu.com/share/link?uk=2705690316&shareid=1025337211&r=9667
- refus:官网免费下载

### 参考教程：
- 通过虚拟机VMware来练习安装ESXi:https://www.cnblogs.com/tielemao/p/5863698.html
- VMware esxi 5.5装机方案： https://www.cnblogs.com/wcwen1990/p/6803669.html
- VMware vSphere虚拟化-VMware ESXi 5.5组件安装过程记录: https://www.cnblogs.com/kevingrace/p/6341259.html
- Vsphere使用： https://www.cnblogs.com/otherside/p/4735236.html

### 注意事项

- 使用软碟通刻录的启动盘会卡住安装界面，建议使用refus。
- 注意，检查并设置bios中intel VT-x功能是否开启，禁用状态无法安装虚拟机。
- 注意网络配置，联系机房管理员，确定服务器的子网掩码和网关地址，避免网络无法连接，以及请求为虚拟机分配静态ip地址
- 默认上载的文件只能给磁盘上的虚拟机使用，即是如放在一块硬盘上的iso镜像文件无法共享给三台虚拟机，进行安装，可指定一个交换区（https://bbs.aliyun.com/detail/511965.html?page=e）但vSphere Client提示会影响性能，考虑到跨硬盘进行页交换可能对性能影响较大，所以不使用这种方式。
- 建议给虚拟机/EXSi所在硬盘预留较大空间（50G以上），传输文件时，虚拟机会使用剩余空间，若满导致scp之类的命令stalled。建议在设置磁盘置备时，选用精简制备，自动增长到所需要的数据空间。
- vSphere 使用安装在win7可以使用，在win10环境下，需要设置兼容性，以win7兼容模式运行，勾选高DPI相关设置，解决鼠标定位不准问题。

### 获取服务器资源信息
查看当前操作系统版本信息
- cat /proc/version
查看物理CPU个数：
- cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
查看每个物理CPU中core的个数(即核数)
- cat /proc/cpuinfo| grep "cpu cores"| uniq

- free -m            #查看内存
- fdisk -l           #查看硬盘分区
- ifconfig           #查看网卡信息

查看网卡速度(root)
- ethtool bond0（网卡名）

查看磁盘/卷的总览情况
- lsblk
查看磁盘是否为ssd
- lsscsi

查看服务器DNS
- cat /etc/resolv.conf







# ubuntu 环境设置

代理工具：[clash for windows](https://github.com/Fndroid/clash_for_windows_pkg/releases)，需要ubuntu手动设置系统代理http，  ip，端口
> [【ubuntu】系统代理的设置](https://blog.csdn.net/u011119817/article/details/110856212)


输入法： 搜狗依赖低版本fcitx版本，默认版本过高，手动安装fcitx5, 使用其他输入法（maybe 退使用低版本更好） 
 > [ubuntu22.04安装中文输入法问题及解决集合](https://zhuanlan.zhihu.com/p/563224248)

多设备鼠标键盘共享: [barrier](https://github.com/debauchee/barrier)
> [神器！多台计算机共享使用键盘鼠标！](https://zhuanlan.zhihu.com/p/438815960)


终端： [terminator](https://gnome-terminator.readthedocs.io/en/latest/gettingstarted.html)

> https://segmentfault.com/a/1190000014992947
> https://zhuanlan.zhihu.com/p/346665734


# 问题

## 声音无输出

参考了这篇文章， 设置 options snd-hda-intel dmic_detect=0 ，在我的gtr7机器上，耳机输出成功。

https://www.myfreax.com/fix-no-sound-dummy-output-issue-in/


tips:

- win(super) + v 快捷键取消日历快捷键，避免习惯误触

> 设置 > 键盘 > 键盘快捷键 > super + v 搜索


## freeing initrd memory on virtualbox

AMD® Ryzen 7 7840hs w/ radeon 780m graphics × 16 

相关问题描述：

- [Unable to install CentOS](https://forums.virtualbox.org/viewtopic.php?p=544077#p544077)

- [Ideapad 5 Pro R7-7840HS VM virtualization issue](https://forums.virtualbox.org/viewtopic.php?t=110964)

linux修复方法类似：

```
cd /usr/lib/virtualbox/

# "ubuntu22.04.04" 有 virutial machine name
./VBoxManage setextradata "ubuntu22.04.04" "VBoxInternal/CPUM/HostCPUID/80000006/edx" "0x00009040"

```

- [Linux中获得AMD显卡的状态信息](https://www.small09.top/posts/210719-gpuinfoinlinux/)
    - amd 查看gpu 工具： radeontop，类似nvidia-smi工具，但是独立显卡，核显查看不了 
        - 实际可以，如果查看不了，可能是amdgpu 模块未加载 
        - `lsmod | grep amdgpu ` 检查 AMDGPU 模块是否已加载, 之后 `lspci -v -s <xx> ` 命令也可以检查使用了amdgpu
        - `sudo modprobe amdgpu` 手动加载 AMDGPU 内核模块 （会注销用户）
    - 另一个监控工具 [amdgpu_top](https://github.com/Umio-Yasuno/amdgpu_top)

    - [ollama: Enable AMD iGPU 780M in Linux](https://github.com/ollama/ollama/pull/5426/files#diff-7ee7b1925642f957e6b8274a2abdd37661c060e369669cbe8e6dad6cddf01bc2) 有人折腾出用 780M 核显 运行 llm 模型




# 技巧

## Ubuntu22.04 注意使用 Xog11 (腾讯会议， 各远程桌面)

默认 Wayland 很多程序不怎么支持。

## 调整swap大小

现在的个人主机内存，也很容易32G, 64G。但是依然可能满足不了开发需要，比如分析jvm dump文件，idea等占用依然出现机器卡住等情况。此时可以调整，swap大小，现在按照的Ubuntu, 一般默认swap大小只有2G。相较物理内存太小。大内存机器，内存和swap可以调整到1:1 或者1:1.5。 一般对 swap 批评可能是交换内存引起卡顿，对服务性能有影响。但是这在个人机器上，个人实际感知不到。

```shell
# 查看当前的swap分区和使用情况
sudo swapon --show

# 禁用swap
sudo swapoff /swapfile

#创建新的swap文件 /swapfile32g
sudo mkswap /swapfile32g

# 启用
sudo swapon /swapfile32g

# 永久性修改，重启机器后生效
sudo vi /etc/fstab


UUID=xxxx-xxxx /    ext4   errors=remount-ro 0       1
/swapfile32g  none  swap  sw  0  0

```







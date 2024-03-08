
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



# 声音无输出

参考了这篇文章， 设置 options snd-hda-intel dmic_detect=0 ，在我的gtr7机器上，耳机输出成功。

https://www.myfreax.com/fix-no-sound-dummy-output-issue-in/


tips:

- win(super) + v 快捷键取消日历快捷键，避免习惯误触

> 设置 > 键盘 > 键盘快捷键 > super + v 搜索


# 技巧

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







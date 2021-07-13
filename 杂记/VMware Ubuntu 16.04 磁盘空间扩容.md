# VMware Ubuntu 16.04 磁盘空间扩容

主要参考文章：[Vmware Ubuntu 16.04 虚拟机磁盘扩容方法](https://blog.csdn.net/liuxd3000/article/details/90729981)

步骤：

- 删除所有备份
- 调大最大磁盘空间大小(100G)
- 创建备份，防止误操作
- 删除当前的3个分区
- 重新创建根分区(96G)，扩展分区(4G)
- 扩展分区上创建交换分区
- 设置启动分区，保存
- 重启
- 解决交换分区UUID变更，导致虚拟机重启需要等待1分30秒问题
  - ls -l /dev/disk/by-uuid/ 查看 分区id，就一个
  - 修改swap分区UUID，/etc/fstab，发现ext4 分区正确，改成和ext4一样的即可
- 重启



## REF

- [Vmware Ubuntu 16.04 虚拟机磁盘扩容方法](https://blog.csdn.net/liuxd3000/article/details/90729981)
- [UBUNTU uuid编辑解决重建swap分区，找不到导致的开机慢问题](https://blog.csdn.net/weixin_37944830/article/details/84710833)




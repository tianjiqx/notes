## Vim8 安装

18年配置的vim-go环境，十分卡，不得不升级到vim8。自己的虚拟机环境还是Ubuntu 16.04LTS，所以参考了这个教程**[install-vim-from-sources-ubuntu.sh](https://gist.github.com/shaypal5/4decf299db737dc66de0647a5d58f96a)**自己编译了vim8.2 。 vim8.2 没有使用教程clone master而是，[release](https://github.com/vim/vim/releases) v8.2.3092。

注意：

- 我将vim80 改成了vim82，虽然之前不存在/usr/local/share/vim 目录。
- 第5步没有成功，我的vim 没有在/usr/bin/vim 而是/usr/local/bin/vim， 并且也没有/usr/bin/vi。 需要更新实际路径为/usr/local/bin/vim， 并且增加/usr/bin/vim配置（for git调用编辑器）。 
  ```shell
  sudo update-alternatives --install /usr/bin/editor editor /usr/local/bin/vim 1
  sudo update-alternatives --set editor /usr/local/bin/vim
  sudo update-alternatives --install /usr/bin/vi vi /usr/local/bin/vim 1
  sudo update-alternatives --set vi /usr/local/bin/vim
  
  sudo update-alternatives --install /usr/bin/vim vim /usr/local/bin/vim 1
  sudo update-alternatives --set vim /usr/local/bin/vim
  ```

升级到vim8之后，没做任何.vimrc 改变，就已经可以正常用vim 浏览tidb的源码了，并且vim-go也生效了。



## Vim-go

vim-go是一个使用golang语言进行开发的vim插件，将vim搭建为合适golang的IDE环境。
插件完整名`Plugin 'fatih/vim-go'`,具体配置参考workspace仓库的.vimrc。



## vim-go 基本使用

vim中已将leader设置为`,`，`let mapleader=","`。
- ,+r  运行 go run
- ,+b  运行 go build
- ,+t  运行 go test


- **Ctrl+]  跳转到定义处**
- ,+ds  跳转定义处并水平分割显示
- ,+dv  跳转定义处并垂直分割显示


- **Ctrl+o 后退**
- **Ctrl+i  前进/Ctrl+t**


- **,+s    显示接口实现**(个人在虚拟机环境使用过慢，更常使用的是ag关键字查找) 


- **:ts 存在多处定义时**  

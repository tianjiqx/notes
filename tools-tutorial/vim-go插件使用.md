## Vim-go
vim-go是一个使用golang语言进行开发的vim插件，将vim搭建为合适golang的IDE环境。
插件完整名`Plugin 'fatih/vim-go'`,具体配置参考workspace仓库的.vimrc。


## vim-go 基本使用
vim中已将将leader设置为`,`,`let mapleader=","`。
- ,+r  运行 go run
- ,+b  运行 go build
- ,+t  运行 go test


- **Ctrl+]  跳转到定义处**
- ,+ds  跳转定义处并水平分割显示
- ,+dv  跳转定义处并垂直分割显示


- **Ctrl+o 后退**
- **Ctrl+i  前进/Ctrl+t**


- **,+s    显示接口实现**(个人在虚拟机环境使用过慢，更常使用的是ag关键字查找) 




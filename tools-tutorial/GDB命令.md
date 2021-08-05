# GDB命令

GDB 作为一个调试工具，支持调试C、C++，Go，Rust程序。



## 基础

- 启动
  - `gdb -p <pid>` 附加到进程
  - `gdb <program> <core dump file>` 调试core文件
- 交互命令
  - `b <path/file>:<lineNumber>  ` 设置断点
    - `b func` 在函数func()的入口处设置断点
    - `info b` 查看已经设置的断点信息
    - `d <number>` 删除断点
    - `disable/enable <number> `  取消/开启 断点
  - `n` 单步执行
    - `n <count>` 执行count次单步
  - `s` 步入函数
  - `c` 继续执行，直到要下个断点（可以用Ctrl+C终止）
  - `u` 运行，直到退出循环体
    - `u <lineNumber>` 运行到某行
  - `p`打印信息
    - `p <varname>` 打印当前栈变量
      - `p file::variable` 打印文件静态变量
      - `p funciton::variable` 打印函数静态变量
    - `p <expr>` 打印表达式结果（成员、函数调用）
    - `info locals` 显示当前堆栈页的所有变量
    - `p/s`  以string 方式打印，如果遇到指针是指向的是字符串
  - `l`  列出源码（默认10行）
    - `l <lineNumber>` 列出行号前后10行代码
    - `layout src` **显示源代码窗口**
    - `l -line <lineNumber>` 显示指定行代码
  - `bt` 显示当前调用堆栈
    - `bt <count>` 显示前count帧
  - `f` 打印当前帧
    - `f <frameNumber>` 显示指定帧
    - `info args` 显示当前帧的参数
  - `q` 退出调试



## GDB for Rust

- `set print pretty on` 设置打印变量格式化更详细友好





## REF

- [GDB 官网 用户手册](https://www.gnu.org/software/gdb/documentation)
- [GDB 中文教程](https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/gdb.html)


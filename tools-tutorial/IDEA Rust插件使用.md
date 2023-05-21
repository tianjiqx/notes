# IDEA Rust插件使用

## IDEA快捷键

- **Ctrl+Alt+L** - 格式化代码，个人对rust文件新增配置**'Shift' + 'F'** （注意配置为使用rustfmt进行格式化，而非IDE内置的格式化工具）
- **Alt + F7** - Find Usage查找符号使用
- **Ctrl + 鼠标左键/Ctrl + B** - 跳转到定义 
- **Ctrl + Alt+B** - 跳转到实现，显示 trait 元素（方法、常量和关联类型）的实现列表。
- **Ctrl + Alt + <- / ->**  -  回退/前进 位置
  - 个人增加配置 **Ctrl + Alt + Shift <- / ->**  

## Rust Tools Tips

**镜像配置工具crm:**

 `cargo install crm`

自动切换到最优的镜像: `crm best`

**GDB调试工具：**

- idea 社区版只支持运行，不支持调试模式，旗舰版支持。

- [gdbgui](https://github.com/cs01/gdbgui)  通用的GDB可视化工具，支持Rust，C++，go。
  
  - 简单在分析TensorBase(Rust)的源码时使用，可以关联源码和进程，设置断点，可以使用。使用示范参见[TensorBase-笔记](https://github.com/tianjiqx/notes/blob/master/big_data_system/TensorBase-%E7%AC%94%E8%AE%B0.md)

- VS code (Code LLDB)
  
  - 个人环境VS卡死未使用

## Q&A

1. Ubuntu 20.04 编译rust项目失败“error: linker `cc` not found”
   
   `sudo apt install build-essential`


## mysql5.7 连接处理流程

该文档，将分析mysql5.7.24(5.7最后一个版本，网上其他关于5.7的连接处理源码分析与当前版本略有出入)的连接处理流程，涉及到客户端发起连接的，发送查询到mysql服务端的整个处理流程，查询解析，优化流程暂略。


###  函数调用图

[5.7.24连接处理函数调用流程](https://github.com/tianjiqx/notes/blob/master/mysql5.7%E8%BF%9E%E6%8E%A5%E6%89%A7%E8%A1%8C%E8%BF%87%E7%A8%8B.pdf)


### 参考文章

- [MySQL · 源码分析 · 网络通信模块浅析](http://mysql.taobao.org/monthly/2016/07/04/)
- [MySQL · 特性分析 · 线程池](http://mysql.taobao.org/monthly/2016/02/09/)
- [MySQL · 性能优化 · thread pool 原理分析](http://mysql.taobao.org/monthly/2014/12/03/)


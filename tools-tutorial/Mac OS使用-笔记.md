# Mac OS使用-笔记

- 跳转
  
  - `command + <- / ->`

- 截图
  
  - `command+shift+4`

- 锁屏
  
  - `Ctrl + Command + Q`

- 软件包管理工具 brew
  
  - 搜索软件：`brew search mysql`
  - 安装： `brew install mysql@5.7`
  - 启动服务：`brew services start mysql@5.7`

- 资源搜索工具：Alfred

- 终端zsh / oh-my-zsh
  
  - `command + T` 新标签页
  - `command + N` 新窗口
  - `Shfit + Home` 跳到行首
  - `Shfit + End` 跳到行尾
  - `Alt + <- / ->` 按词组跳

- 前往文件夹，允许访问根目录(Go to the folder)：command+shift+g，然后直接输入目录

- 检测端口
  
  - `nc -vz -w 2 localhost 2181`
  
  - - -v 详细信息
    - -z 不发送包给对方
    - -w 后面是数字，秒，表示多少时间结束，不等太长时间。
    - -u udp 协议，默认是tcp。上图可以看到。如果是dns端口检测，用u

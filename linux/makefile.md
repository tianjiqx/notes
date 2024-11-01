## Tips

```makefile
# 获取当前路径
MAKEFIE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURDIR:=$(shell dirname $(MAKEFIE_PATH))

# 获取操作系统版本，
ARCH:="$(shell uname -s)"
LINUX="Linux"
MACOS="Darwin"
WINDOWS="Windows_NT"

.PHONY: a1 a2
.ONESHELL:

SHELL=/bin/bash

a2: a1
ifeq ($(ARCH), $(WINDOWS))
    echo "window"
else
    echo "linux/macos"
endif
```

```
# 忽略原始命令
make -s <targetName> 

# @ 开头命令忽略单条原始命令
@echo "xxx"
```

语法规则

```
targets : prerequisites
    command
    ...
```

- targets 文件名/伪目标

- prerequisites 依赖文件

## REF

-  [跟我一起写Makefile](https://seisman.github.io/how-to-write-makefile/index.html)

- [11 个 Makefile 实战技巧 - 掘金](https://juejin.cn/post/6844903917499711496)

- [makefile + conda](https://stackoverflow.com/questions/53382383/makefile-cant-use-conda-activate)

- [Makefile学习笔记; 显示/隐藏命令 忽略命令错误](https://blog.csdn.net/LGibsion/article/details/70854565)

- https://stackoverflow.com/questions/53382383/makefile-cant-use-conda-activate

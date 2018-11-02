
## Sed


sed是与grep和awk被称为liunx三剑客，是一个有用的文本处理工具，个人多数用来截取文本内容,批处理。注意都不会改变原文件，若需保持，可重定向到新的文件中。

### 用法

- 语法：sed [OPTION]... {script-only-if-no-other-script} [input-file]...
- [option]说明：
  - n ：仅显示处理后的结果
  - f ：指定处理脚本
  - e ：多点编辑，每个-e表示一个处理命令
- 打印指定范围的行：sed '2,4p' filename / sed '10,$p' /sed '^,10p'  
- 打印包含正则pattern(errors)的行：Sed –n ‘/errors/p’ filename
- 搜索并替换(1-100行范围内的,起始行为1)： sed '1,100s/old/new/g' 
- 删除：sed '2,5d' filename 
- 搜索并删除：sed -n '/pattern/d'
- 数据的搜寻并执行命令：nl /etc/passwd | sed -n '/root/{s/bash/blueshell/;p;q}' (搜索/etc/passwd,找到root对应的行，执行后面花括号中的一组命令，每个命令之间用分号分隔，这里把bash替换为blueshell，再输出这行,最后退出)
- 增加(第2行后增加xxx)：sed '2a xxx'
- 增加(第2行前增加xxx)： sed '2i xxx'
- 替换多行(2-4行替换为字符串)： sed '2,5c represent 2-5 line'



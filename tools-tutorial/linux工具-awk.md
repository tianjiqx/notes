## AWK

awk是一个可编程的文本处理、分析工具，相对与sed而言，具有更大的可操作性。

### 用法：

- 基本语法： awk [option] 'script'  filename

- 选项说明：
  
  - F ： 指定文件域分隔符（默认为tab或空格）
  - f ： 从脚本文件中读取awk命令
  - v ： 设置一个用户定义变量

- 内置变量：
  
  - $n：当前第n个字段,$0 为全部记录
  - FS：输入字段分隔符号，默认空格和tab
  - OFS：输出字段分隔符：默认空格
  - RS： 输入记录（行）分隔符，默认换行符
  - ORS：输出记录（行）分隔符，默认换行符
  - NF：当前记录（行）字段个数
  - NR：行号，当前文本行行号
  - FNR：各个文件分别计数的行号
  - ARGC：命令行参数个数
  - ARGV：数组，命令行给定参数

- 打印：
  
  - 打印一行全部内容： awk '{print $0}'
  - 打印一行的第1,4项：awk '{print $1,$4}'
  - 格式化输出 awk '{printf "|%-5s |%-10s |\n" ,$1,$4}'
  - 使用‘，’作为分隔符： awk -F, '{print $1,$2}' / awk 'BEGIN{FS=","} {print $1,$2}'
  - 使用‘:’作为分割符号打印一行各段：awk -F: '{for(i=1;i<=NF;i++){print $i}}'
  - 输出第二列包含 "th"，并打印第二列与第四列(~表示模式开始。// 中是模式)：awk '$2 ~ /th/ {print $2,$4}'
  - 模式取反：awk '$2 !~ /th/ {print $2,$4}'
  - 忽略大小写：awk ' BEGIN{IGNORECASE=1} /this/ '

- 控制流程语句：
  
  - if：awk '{} if ( $2 >10 ) { } else { } }' 
  - for：awk '{for(i=0;i<10;i++)  { print i } }'
  - while：  awk '{  i=0; while(i<6) {print i;i++} }'
  - break/continue
  - exit：退出程序

- 数组（map）：
  
  - 格式：array_name[index]=value
  - 创建与访问： awk '  BEGIN{ arr["abc"]="xxx" ;arr["def"]="123" ; print arr["abc"]; delete arr["abc"]; } '

- 自定义函数：
  
  - 语法： function function_name([arg1,arg2,...]){}
  - min： 'function min(a,b){  if (a>b) {return a} return b; }  BEGIN {print min(10,11)} '

- 内置函数：
  
  - match(str,Ere)：正则匹配，返回值为出现位置，未找到返回0
  - substr(str, start, len)：截取子串
  - length(str)：返回字符串的长度

- 脚本：
  
  - 执行脚本： awk -f script filename
  - BEGIN{执行前的语句}
  - END{执行后执行的语句}
  - {每行处理时执行的语句}



```shell
# 1. 计算每行长度，并递减排序
awk  '{print length($0)}' /log/hadoop_template1.log | sort -n -r | head


# 2. 每行求和

| awk '{sum+=$1} END {print sum}'


# 3. 采样 
awk 'NR % 10 == 0' input.txt

```

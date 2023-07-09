# shell 编程



```
# 数组定义

arr=(
app-1669115373984
app-1664193528246
)

# 数组遍历
for it in ${arr[*]};
do
  echo "value: $it"
done



# 括号
1. () 开启子shell执行命令 $( echo "xxx") ; 数组初始化
2. (()) 整数型的计算，不支持浮点型
3. [] 
4. [[ ]]  


# if [] 
[-z STRING] “STRING” 的长度为零则为真。


```



## REF

- [shell 中判断语句 if 中 - z 和 -n](https://www.cnblogs.com/pugang/p/13167714.html)





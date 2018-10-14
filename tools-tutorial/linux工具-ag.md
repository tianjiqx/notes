
## AG
ag是一个强大的linux搜索工具，可以用来分析源码，搜索文件名，速度极快。

## 常用命令
- 基本命令规范： ag [FILE-TYPE] [OPTIONS] PATTERN [PATH]
- 搜索目录文件内容：ag "key words" path(默认当前目录)
- 大小写敏感：ag -s "xxx" 
- 反向匹配：ag -v "xxx"
- 全词匹配：ag -w "xxx"
- 非正则匹配搜索：ag -Q "xxx"
- 只搜索文件名： ag -g test (单关键字不需要"")









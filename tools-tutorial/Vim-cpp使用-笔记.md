# Vim-cpp使用-笔记

## vim 配置：

参考个人workspace项目的[.vimrc](https://github.com/tianjiqx/workspace/blob/master/.vimrc)文件



## 关键插件

- ctags - 生成源码标签。完成自动补全、识别函数，变量，函数跳转。

- NERDTree - 文件树

- TagbarToggle - Structure窗口，展示类的各个函数和变量

  



## 快捷键（根据自己vimrc配置后）

- Ctrl + p - 根据文件名，文件搜索
- F10 - 显示/隐藏 NERDTree文件树
- F8 - 显示/隐藏 TagbarToggle界面
  - 点击函数，变量可跳转到定义处
- **Ctrl+] - 跳转到定义处**
- **Ctrl+o - 后退（回到之前的文件鼠标位置）**
- **Ctrl+i  - 前进/Ctrl+t**
- ts <关键字>- 列出匹配关键字的函数、变量 （other 技巧：直接使用ag 搜索关键字，ag -g 搜索文件名）
- ta <关键字> - 直接跳转到第一个匹配关键字的函数、变量
- , + y - 复制选中内容
- , + v - 粘贴选中内容
- 光标移动到单词上 + gd - 高亮单词
- 光标移动到单词上 + Shift + * - 跳转到文件内单词下一次出现的位置（单词可以是变量，函数，类等等）
- 光标移动到单词上 + Shift  + # - 跳转到文件内单词下一次出现的位置 
  - 搜索高亮后，可以用n，跳转到一下个位置。大写N，跳转到上一个



TODO：更现代化的vim8 配置，[如何在 Linux 下利用 Vim 搭建 C/C++ 开发环境? - 韦易笑的回答 - 知乎](https://www.zhihu.com/question/47691414/answer/373700711)

[Vim 8 下 C/C++ 开发环境搭建](http://www.skywind.me/blog/archives/2084)


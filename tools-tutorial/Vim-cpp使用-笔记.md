# Vim-cpp使用-笔记

## vim 配置：

参考个人workspace项目的[.vimrc](https://github.com/tianjiqx/workspace/blob/master/.vimrc)文件

注意，其中配置使用了系统剪切板，可能需要安装

```shell
vim --version | grep clipboard
sudo apt install vim-gtk
```



## 关键插件

- ctags - 生成源码标签。完成自动补全、识别函数，变量，函数跳转。

  - universal-ctags

- NERDTree - 文件树

  - `F10` 显示和折叠
  - `O` 递归展开当前光标目录下所有文件
    - `o` 打开或者折叠目录

  - `X` 递归合并当前光标目录下所有文件
  - `P`  跳到根节点
    - `p` 跳到父节点

  - `U`  设置上级目录为根目录,并维持当前目录打卡状态
  - `C` 将当前光标目录设置为根目录 (很卡)
  - `:NERDTreeFind<cr>`   打开文件所在目录

- TagbarToggle - Structure窗口，展示类的各个函数和变量

  - `F8` 显示和折叠

- LeaderF 模糊搜索

  - `Ctrl + P` 搜索文件名
  - `Ctrl + N` 搜索最近打开文件
  - `F5` 当前文件（缓冲）搜索函数
    - `:LeaderfFunction` 进入搜索函数
    - `<M+p>` M 表示meta，一般是alt/option （macos， 终端需要配置允许option为meta键）

  - `F6` 当前缓冲区总搜索关键字，显示所有候选模糊匹配的关键字
    - `:LeaderfLine`  进入按行搜索关键字
    - 可支持多个词

  - `ESC` 从leaderf 模式退出

- Ack 

  - `:Ack [options] {pattern} [{directories}]`配置在vim 中进行ag 搜索
  - `:Ack!` 将鼠标放在关键词上，在当前目录搜索该词
    - 模拟IDE findusage
    - `,+A` 快捷键


  

## 快捷键（根据自己vimrc配置后）

- Ctrl + p - 根据文件名，文件搜索
- F10 - 显示/隐藏 NERDTree文件树
- F8 - 显示/隐藏 TagbarToggle界面
  - 点击函数，变量可跳转到定义处
- **Ctrl+] - 跳转到定义处**
- **Ctrl+o - 后退（回到之前的文件鼠标位置）**
- **Ctrl+i  - 前进/Ctrl+t**
- :ts <关键字>- 列出匹配关键字的函数、变量 （other 技巧：直接使用ag 搜索关键字，ag -g 搜索文件名）
  - 或者鼠标移动到函数，类名字上，`:ts!<CR>`

- :ta <关键字> - 直接跳转到第一个匹配关键字的函数、变量
- , + y - 复制选中内容
- , + v - 粘贴选中内容
- 光标移动到单词上 + gd - 高亮单词
- 光标移动到单词上 + Shift + * - 跳转到文件内单词下一次出现的位置（单词可以是变量，函数，类等等）
- 光标移动到单词上 + Shift  + # - 跳转到文件内单词下一次出现的位置 
  - 搜索高亮后，可以用n，跳转到一下个位置。大写N，跳转到上一个



`noremap` 查看normal 模式快捷键



TODO：更现代化的vim8 配置，[如何在 Linux 下利用 Vim 搭建 C/C++ 开发环境? - 韦易笑的回答 - 知乎](https://www.zhihu.com/question/47691414/answer/373700711)

[Vim 8 下 C/C++ 开发环境搭建](http://www.skywind.me/blog/archives/2084)

[将vim与系统剪贴板的交互使用](https://zhuanlan.zhihu.com/p/73984381)




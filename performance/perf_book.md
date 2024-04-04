

# Performance Analysis and Tuning on Modern CPU


测量工具 [temci](https://github.com/parttimenerd/temci)

自动化性能回归测试框架
- https://github.com/JoeyHendricks/STATS-PAL
- https://github.com/evergreen-ci/evergreen





## REF
- [github: perf-book](https://github.com/dendibakh/perf-book)
    - tex 文本，如果是Ubuntu 22.04系统，miktex 似乎还是无法工作（遇到`qt.qpa.plugin: Could not find the Qt platform plugin "xcb" in "/usr/lib/x86_64-linux-gnu/qt5/plugins"`），建议 执行 python export_book.py 之后，生产book.tex之后，使用 texmaker 打开 book.tex 文件， 构建，打印出 pdf
    ```
    # 安装完全版 latex 软件 texlive
    sudo apt-get install texlive-full
    # 安装可视化工具 texmaker
    sudo apt-get install texmaker
    ```
 

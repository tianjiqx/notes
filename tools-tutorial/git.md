## Git 常用

- fork 项目
  
  ```shell
  git remote add upstream https://github.com/pingcap/tidb.git
  git remote set-url --push upstream no_push
  git remote -v
  # 修改
  git remote set-url <remote_name> <remote_url>
  
  # 拉取远程分支到本地
  git pull origin <远程分支名>:<本地分支名>
  ```

- 同步远程分支
  
  ```shell
  git fetch upstream
  git checkout master
  git rebase upstream/master  (将本地提交回退形成补丁，更新到upstream/master分支的代码后，应用这些补丁，可以加-i参数进行压制提交)
  如果遇到冲突，则查看冲突文件并解决，然后执行以下两条命令
  git add <冲突文件>
  git rebase --continue
  ```

- 修改代码并提交到本地, 压制提交，合并提交
  ```shell
  git add .
  git commit -m "WARP-0000: xxxx"  
  git rebase -i HEAD~3 (管理最近三次commit)
  间隔合并多个commit，只需要将要压制的commit排序到想要保留的commit下面
  ```

- 比较
  ```
  git diff  (临时区)
  git diff --cached (暂存区)
  git diff commit1 commit2 (对比commit版本)
  ```
- 修改commit log
  ```
  git commit -- amend  (最近一次commit信息)
  解决使用git commit -- amend已提到远程仓库的commit，产生“您的分支和 'origin/master' 出现了偏离”问题，恢复到远程状态
  git reset --hard old commit
  提示你落后远端分支
  git status
  重新从远端pull
  git pull
  查看状态，您的分支与上游分支 'origin/master' 一致
  git status
  ```
- 拉取tag分支
  ```
  git fetch upstream  
  列出所有tag
  git tag
  切换到tag
  git checkout <tag-name>
  创建对应分支
  git checkout -b <tag-name>
  ```

- cherry-pick 将其他分支的提交，追加到本地
  ```
  git cherry-pick  <commid_id1> <commid_id2>
  ```

- 打patch，应用path
  
  ```
  生成最近的1次commit的patch
  git format-patch HEAD^
  生成最近的2次commit的patch
  git tch HEAD^^　　　　　　
  生成两个commit间的修改的patch（包含两个commit. <r1>和<r2>都是具体的commit号)
  git format-patch <r1>..<r2>          
  生成单个commit的patch
  git format-patch -1 <r1>                                                 
  生成某commit以来的修改patch（不包含该commit）
  git format-patch <r1> 
  
  将名字为0001-limit-log-function.patch的patch打上
   git am 0001-limit-log-function.patch  
   保证特殊字符[] 的提交信息不丢失
   git am --keep-non-patch 0001-limit-log-function.patch  
   将路径~/patch-set/*.patch 按照先后顺序打上
   git am ~/patch-set/*.patch　　　　　　　　　　　
  
  当git am失败时，可以将已经在am过程中打上的patch废弃掉(比如有三个patch，打到第三个patch时有冲突，那么这条命令会把打上的前两个patch丢弃掉，返回没有打patch的状态)
   git am --abort
  
  发生冲突,也可以强行打这个patch，发生冲突的部分会保存为.rej文件（例如发生冲突的文件是a.txt，那么运行完这个命令后，发生conflict的部分会保存为a.txt.rej），未发生冲突的部分会成功打上patch, 根据.rej文件，通过编辑该patch文件的方式解决冲突。
   git apply --reject <patch_name>
  
  解决冲突后,删除.rej文件，添加修改后的进去
   git add <filename>
  
  标记解决/ 继续 完成应用
   git am --resolved / git am --continue
  ```

- 信息调整
  
  ```
  限制克隆大小
  只保留最新一次提交记录，其余历史提交信息抛弃  
  git clone --depth 1 
  
  修改最近一次git提交时间,用户
  `git commit --ammend --date="23 Nov 2021 14:00:24 +0800"`
  `git commit --amend --author="xx <xx@xx.com>"`
  ```

- 暂存
  
  ```
  git stash 暂存修改
  git stash apply 应用最近的暂存
  git stash list 查看暂存
  git stash show -p stash@{0} 查看暂时内容
  ```

- git config
  
  ```
  git config [--global] user.name "Full Name"`
  git config [--global] user.email "email@address.com"
  git config --list
  ```

- 查看提交变更文件
  
  `git log --stat`

- 拉取别人的PR到本地
  
  `git fetch upstream pull/<ID>/head:<BRANCHNAME>`


- 忽略已经在remote的文件/目录
  ```
  .gitignore 
  # Ignore .idea files
  .idea/


  git add .gitignore
  git commit -m "Add .gitignore to ignore .idea/"

  # 查找被track的文件
  git ls-files -v | grep "\.idea"

  # 停止跟踪
  git rm -r --cached .idea/

  # 提交更改
  git commit -m "Untrack .idea files"
  git push

  ```
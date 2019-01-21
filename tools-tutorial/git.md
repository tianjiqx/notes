## Git 常用

- fork 项目

  git remote add upstream https://github.com/pingcap/tidb.git

  git remote set-url --push upstream no_push

  git remote -v

- 同步远程分支

  git fetch upstream

  git checkout master

  git rebase upstream/master  (将本地提交回退形成补丁，更新到upstream/master分支的代码后，应用这些补丁，可以加-i参数进行压制提交)

  如果遇到冲突，则查看冲突文件并解决，然后执行以下两条命令

  git add <冲突文件>

  git rebase --continue

- 修改代码并提交到本地

  git add .

  git commit -m "WARP-0000: xxxx"

- 压制提交，合并提交

  git rebase -i HEAD~3 (管理最近三次commit)

- 比较

  git diff  (临时区)

  git diff --cached (暂存区)

  git diff commit1 commit2 (对比commit版本)

- 修改commit log

  git commit -- amend  (最近一次commit信息)

  解决使用git commit -- amend已提到远程仓库的commit，产生“您的分支和 'origin/master' 出现了偏离”问题，恢复到远程状态

  git reset --hard old commit

  提示你落后远端分支

  git status

  重新从远端pull

  git pull

  查看状态，您的分支与上游分支 'origin/master' 一致

  git status


  

#new local rep
mkdir local_rep_name && cd
git init
git add
git commit -m ""
git remote add origin URL
git push -u origin master

#add local change file
#change
git add
git commit -m ""
git pull --rebase
git push -u origin master


git pull URL
git pull --rebase origin master
git push -u origin master

#maybe help
git remote set-url origin https://github.com/kaka7/marathon.git
git remote rm origin
git remote add origin https://github.com/kaka7/marathon.git
git remote -v

git pull = git fetch + git merge
git pull --rebase = git fetch + git rebase
git status




Sed 

```sh
1,20s/old/new/g 就是啦！1到20行 
sed 's/要被取代的字串/新的字串/g'
nl /etc/passwd | sed -e '3,$d' -e 's/bash/blueshell/'
[root@www ~]# sed -i '$a # This is a test' regular_express.txt
先grep出来 -rn行号
```
 
Lsof

    使用-i:port来显示与指定端口相关的网络信息
    使用@host来显示指定到指定主机的连接
    使用@host:port显示基于主机与端口的连接
    找出监听端口
    lsof -i -sTCP:LISTEN 
    Grep 也可
    lsof -i -sTCP:ESTABLISHEＮ
    Lsof -u ^user
    1   # kill -9 `lsof -t -u daniel`
    # lsof -u daniel -i @1.1.1.1
 
##good CMD
```
dir（func）    
Func.__doc__
info ps ;man -k df
jupyter nbconvert --to python *.ipynb 
ipython转换为pdf格式
mypackage/__init__.pymypackage/mymodule.py
uname -rdpkg -l | grep linux-image-sudo apt-get remove
export SPARK_HOME="$(cd "`dirname "$0"`"/..; pwd)"
export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bashrc
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock
sudo mv /var/lib/dpkg/info /var/lib/dpkg/info.bak //现将info文件夹更名
sudo mkdir /var/lib/dpkg/info //再新建一个新的info文件夹
sudo apt-get update// 不用解释了吧
apt-get -f install xxxsudo mv /var/lib/dpkg/info/* /var/lib/dpkg/info.bak//执行完上一步操作后会在新的info文件夹下生成一些文件，现将这些文件全部移到info.bak文件夹下
sudo rm -rf /var/lib/dpkg/info //把自己新建的info文件夹删掉sudo mv /var/lib/dpkg/info.bak /var/lib/dpkg/info //把以前的info文件夹重新改回名字
 
同时支持Python2(已安装)和Python3 jupyter notebook
python3 -m pip install ipykernel
python3 -m ipykernel install --user
 
进入python，执行help('modules')
grep -C 3 string filename.txt
for user in $(cut -f1 -d: /etc/passwd); do echo $user; crontab -u $user -l; done
sudo apt-get --purge remove linux-image-3.18.0-67-generic
Who,w -i
如果你需要的字符串以指定字符串开头，可以使用它，如：
$ look hell | head -11    
gsettings set com.canonical.Unity.Launcher launcher-position Bottom
 
源冲突，先删除，然后重新安装
包在/var/cache/apt/archives,没有下载完的在/var/cache/apt/archives/partial
dpkg --get-selections|grep linux
cp -i
groupadd -G -a  gid gname;
useradd -u 1988 -g 1000 john;usermod -G group
硬链接由于采用的是指针的方式，如果文件删除，它将一直指向已删除的文件，而软链接总是指向新创建的文件
at now+5 minutes
//不带引号，输出的是变量内容
root@sparkmaster:~/ShellLearning/chapter09# echo $JAVA_HOME
/hadoopLearning/jdk1.7.0_67
//双引号，输出的也是变量内容
root@sparkmaster:~/ShellLearning/chapter09# echo "$JAVA_HOME"
/hadoopLearning/jdk1.7.0_67
//单引号的话，内容原样输出，不会解析变量值 字符宜用单引号
root@sparkmaster:~/ShellLearning/chapter09# echo '$JAVA_HOME'
$JAVA_HOME
 
自定义变量具有只能在当前进程中使用，当开启子进程时，变量在子进程中不起作用，如果需要父进程中定义的变量在子进程中也能够使用，则需要将其设置为环境变量，环境变量使用export命令进行定义
root@sparkmaster:~/ShellLearning/chapter09# echo "$first*$second" | bc
35.7
cmd 2>stderr.txt 1>stdout.txt
命令别名，alias install='sudo apt-get install'
//但是需要注意的是在终端取别名，一旦终端关闭，别名命令不会保存
//如果想永久使用即开机后该别名命令就生效的话，则需要将别名命令重定向
//保存到~/.bashrc文件中
root@sparkmaster:~/ShellLearning/chapter11# echo 'alias install="sudo apt-get install"' >> ~/.bashrc
read -p "pleas input a number:" -s  num[敲回车]
dpkg --list | grep linux-image
df --help
info bash
man -k df
help [list]
源冲突，先删除，然后重新安装
ALT+F2
dpkg --list | grep linux-image 
unzip git.zip
雷锋网，简书，推酷，segmentfault,简书
sudo apt-get clean
sudo apt-get update-grub
sudo rm /var/cache/apt/archives/lock 
sudo rm /var/lib/dpkg/lock
Cat test.json | python -m json.tool
 
20181223
r,g,b=src.split()
 
 
from distutils.sysconfig import get_python_lib
print(get_python_lib())
 
sys.path.append('./')
 
http:
get post put delete
curl -X GET 
 
upper = str.upper
unzip -O CP936 资料.zip 
 
data[data[:,2].argsort()]
data[:,data[2].argsort()]  
 
 bb.index(max(bb))
 r u \ \n '''''' [::-1] unicode<-str %e %%
 < file
 while read f
 do 
   echo "line is $f"
done <file
 
cut -d:-f5 /etc/passwd
 
foo='ls'
case $foo in
 a)
 echo
 b)
 esac
 
 func(){
 expr $1\*2
 }
 func 3
 
 if ["$s" -lt "$y"]:then
 echo
 fi
 
 alias l="ls -al"
 
 find  -print/-ls
 awk ... file
 egrep "(foo|bar)" file
 ${var:=value}
  ${var:-value}  ${var:?value}
 
  @app.route('/IINDEX/<user>')
  def func(user)
 
  request.get_json()
   netstat -ntlp


iconv -f ISO-8859-1 -t UTF-8 < input.txt > output.txt
cat tab_delimited.txt | tr "\\t" "," comma_delimited.csv
split -l 500 filename.csv new_filename_
find . -type f -exec mv '{}' '{}'.csv \;
# Sorting a CSV file by the second column alphabetically
sort -t, -k2 filename.csv
# Numerically
sort -t, -k2n filename.csv
# Reverse order
sort -t, -k2nr filename.csv
sort -f ignore case
• sort -r reverse sort order
• sort -R scramble order
• uniq -c count number of occurrences
  uniq -d only print duplicate lines
  cut -d, -f 1,3 filename.csv
  cat filename.csv | cut -d, -f 2 | sort | uniq -c | head
  paste -d ',' names.txt jobs.txt > person_data.txt 列合并
  # Join the first file (-1) by the second column
# and the second file (-2) by the first
join -t, -1 2 -2 1 first_file.txt second_file.txt
grep -lr 'word' . 
grep "first_value\|second_value" filename.csv 递归
• grep -w only match whole words
• grep -l print name of les with match
sed -i '' 's/\$//g' data.txt
sed -i '' 's/\([0-9]\),\([0-9]\)/\1\2/g' data.txt
sed -i '' '/jack/d' data.txt  delete
awk -F, '/word/ { print $3 "\t" $4 }' filename.csv
awk -F, ' $1 == "string" { print NR, $0 } ' filename.csv
awk -F, ' $3 >= 2005 && $5 <= 1000 { print NR, $0 } ' filename.csv
awk -F, '{ x+=$3 } END { print x }' filename.csv
awk -F, '$1 == "something" { x+=$3 } END { print x }' filename.csv
grep -rn
tar -tvf
lsof filename
ls -s
sort -k5n | tail -5
uniq -c 
pip install git+*.git
ps -aux | sort -rnk 4
mount -o remount ,rw /
cnn sites:pan.baidu.com
curl _I -s app:5000
curl database:27017
lsof -p pid
lsof -i tcp:80
netstat -tdpn
tar -uf增量
tar -rf增量
date +%Y.%.%d-%
awk -F ',' {print $1}'


R
Ｒ自动生成报告ｋｎｉｔｒ；ｒｍｄ；ｇｇｖｉｓ到ｇｇｐｌｏｔ２网页，ｓｏｕｒｃｅ（“”）加载文件
 
Office
Ｅｘｃｅｌ：ｓｈｉｆｔ＋Ｆ８选定不连续的单元格
 
Linux
并发;cpu时间切片，轮流分给不同的进程（具体来时就是某个进程的thread）分时使用
 
VI正则表达式搜索
正则表达式搜索是指加入了像”^,$,.”等特殊匹配字符，它们的作用如下表：
搜索字符串	搜索描述	举例
:/^Spark	搜索以Spark为开头的行	Spark is ….
:/YARN$ 	搜索以YARN为结尾的行	…Hadoop YARN
:/Ha…p	搜索Ha开头，中间有三个字符且以p结尾的字符串	Hadoop、Hadaap
:/e>	查找以e结尾的字符串，其中>符号是字符串结束指示符号，这里\不是转义字符，而是与>组合到一起，来表示特殊意义	like、source
:/\<Had	查找以Had作为开始的字符串，\< 同样具有特殊意义	Hadoop、Hadoo
:/Spa*	查看字符串中出现至少一次Spar的字符串，\< 同样具有特殊意义	Spark、SpaSpark
:/Sp[ae]rk	匹配Spark或Sperk	Spark、Sperk
文本替换使用以下语法格式：
:[g][address]s/search-string/replace-string[/option]
其中address用于指定替换范围，下表给出的是常用示例：
//将当前缓冲区的第一行中的Downloading替换为Download
: 1 s/Downloading/Download
 
//将当前缓冲区中的第一行到第五行中的Spark替换为spark
:1,5 s/Spark/spark
 
//将当前缓冲区中的第一行到当前光标所在行的Spark替换为spark
:1,. s/Spark/spark
 
//将当前光标所在行到缓冲区最后一行的Spark替换为spark
:.,$ s/Spark/spark
 
//将整个缓冲区中的Spark替换为spark
:% s/Spark/spark
 
//当前行中第一次搜索到的Spark替换为spark
: s/Spark/spark
 
//将当前行中所有的Spark替换为spark
:s/Spark/spark/g  
 
//将所有的and转换成And，不包括theta这种字符串，只会作用于the这种单独存在的字符串
:% s/\<the\>/The/g  
 
 
Ø 正则表达式
只有圆括号“()”才能用于形成组。“[]”用于定义字符集。“{}”用于定义重复操作。
当用“()”定义了一个正则表达式组后，正则引擎则会把被匹配的组按照顺序编号，存入缓存。当对被匹配的组进行向后引用的时候，可以用“\数字”的方式进行引用。<<\1>>引用第一个匹配的后向引用组，<<\2>>引用第二个组，以此类推，<<\n>>引用第n个组。而<<\0>>则引用整个被匹配的正则表达式本身。我们看一个例子。


ps –aux
 
request
常用的HTTP动词有下面五个（括号里是对应的SQL命令）。
        GET（SELECT）：从服务器取出资源（一项或多项）。
        POST（CREATE）：在服务器新建一个资源。
        PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
        PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
        DELETE（DELETE）：从服务器删除资源。
还有两个不常用的HTTP动词。
        HEAD：获取资源的元数据。
        OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。
过滤信息（Filtering）
状态码（Status Codes）
Hypermedia API


磁盘坏损处理
测试读写
hdparm -t /dev/sda
ｆｓｃｋ
tune2fs -l /dev/sdb2　文件系统自检
e2fsck -a
用fsck.ext4  -y /dev/sdb2修复是报如下信息
Could this be a zero-length partition
mke2fs -n /dev/sdb2

e2fsck /dev/sdb2 -b 32768
mount: /dev/loop0: can't read superblock错误
tune2fs -l /dev/sdb2
找到Blocks per group后面的数字，我这是32768
fsck.ext4 -b 32768 /dev/sdb2
e2fsck /dev/sdb2 -b 32768

securecrt 
在vt100模式下会delete键和backspace键功能一样，都是删除前面的内容，要调整向后删除需要设置下:会话选项--终端--仿真--终端里选择linux模式即可。

jupyter
2019年8月2日
17:34
网页版　jupyter notebook 权限问题
ipython kernelspec list
ipython kernelspec remove 
json文件
创建新kernel
(hello) babao@babao:~$ sudo python -m ipykernel install --name py3						
						
pycharm启动容易报错,和目标python解释器不一致
/home/naruto/anaconda3c/bin/python /home/naruto/anaconda3c/bin/jupyter-notebook --no-browser --ip 127.0.0.1 --port 8888 --port-retries=0

pip安装：只会生成pythonAPI，但是如果底层不是python则，一步一步跟进时看不到底层语言实现的具体代码，编译安装则可以看到最终的代码
GDB调试机器代码程序，可以看到源码


dpkg apt
rpm yum
源码 make
Pycharm 直接运行
Pip 自动安装依赖 即下载whl 或从github下下来 切换到对应的版本安装 opencv 

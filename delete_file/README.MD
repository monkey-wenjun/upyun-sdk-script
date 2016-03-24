####依赖:

sudo pip install requests

####删除方法:

后台运行:

1.Centos/RedHad
```
   yum -y install screen
   screen -S delete_upyun_file
   python delete_file.py
```

2.Debian/Ubuntu

```
	sudo apt-get install screen
	screen -S delete_upyun_file
	python delete_file.py
```

通过screen在后台运行脚本的好处就是即使本地与远程ssh主机断开后，程序依然能够正常运行
```
	~$ screen -ls #查看当前后台运行的脚本
	There are screens on:
	        3003.test       (03/24/2016 10:58:26 AM)        (Attached)
	        2860.delete     (03/24/2016 10:57:52 AM)        (Detached)
	        6828.py (03/16/2016 08:50:22 PM)        (Detached)
	3 Sockets in /var/run/screen/S-fangwenjun.
	$ screen -r test #进入已经创建的后台任务中
```
### 更新历史

2016-3-24：
1.增加用户交互功能，无需进入脚本输入参数
2.输入密码不可见
3.修复2处可能抛异常的地方



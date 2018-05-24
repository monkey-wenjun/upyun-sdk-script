####依赖:

sudo pip install requests


###视频教程

https://techs.b0.upaiyun.com/videos/cdnpage/delete_file.html


####删除方法:

```
bucket = ''
username = ''
password = ''

path = ''
```

在脚本中填入上述参数。分别是服务名，操作员名，操作员密码，和待删除的路径。

然后 python delete_file.py 进行删除.

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




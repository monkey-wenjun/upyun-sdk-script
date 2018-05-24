####依赖:

sudo pip install requests



####统计目录内文件大小的方法:

```
bucket = ''
username = ''
password = ''

path = ''
```

在脚本中填入上述参数。分别是服务名，操作员名，操作员密码，和待统计的路径。

然后 python count_directory_size.py 进行删除.

后台运行:

1.Centos/RedHad
```
   yum -y install screen
   screen -S count_directory_size.py
   python count_directory_size.py
```

2.Debian/Ubuntu

```
	sudo apt-get install screen
	screen -S count_directory_size.py
	python count_directory_size.py
```

通过screen在后台运行脚本的好处就是即使本地与远程ssh主机断开后，程序依然能够正常运行
```
	~$ screen -ls #查看当前后台运行的脚本

	$ screen -r test #进入已经创建的后台任务中
```




在脚本内部填写:

```
# -----------------------
bucket = ''  # 服务名
username = ''  # 操作员名
password = ''  # 操作员密码

path = '' # 需要列文件列表的起始目录
# -----------------------
```

填写无误后, 直接运行

```
python list_file_with_iter.py

```

如果文件量巨大，也可以使用 screen 工具， 或者 nohup 将进程挂载。

比如：

```
nohup python list_file_with_iter.py &
```

或者:


后台运行:

1.Centos/RedHad
```
   yum -y install screen
   screen -S list_file_with_iter
   python list_file_with_iter.py
```

2.Debian/Ubuntu

```
	sudo apt-get install screen
	screen -S list_file_with_iter
	python list_file_with_iter.py
```

查看 screen
```
	$ screen -ls #查看当前后台运行的脚本
	
	$ screen -r xxxx #进入已经创建的后台任务中
```
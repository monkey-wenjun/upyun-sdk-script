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
	scren -S delete_upyun_file
	python delete_file.py
```
### 更新历史

2016-3-24：
1.增加用户交互功能，无需进入脚本输入参数
2.输入密码不可见
3.修复2处可能抛异常的地方



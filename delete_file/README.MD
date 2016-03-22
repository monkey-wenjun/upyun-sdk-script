####依赖:
sudo pip install requests

####修改:

第96行

```
for path in range(0,10):
    deleteUri("/"+ str(path))
```

这个起始删除的目录需要重新定义.


####删除方法:
后台运行:

```
nohup python delete_file.py &
```


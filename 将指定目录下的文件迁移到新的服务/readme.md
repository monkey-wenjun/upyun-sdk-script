#### 依赖

脚本依赖又拍云 SDK

```
pip install upyun
```

#### 参数说明

使用脚本之前, 需要在脚本第 11 行 和 24 行 填写一下相应的参数。

比如: 我要从 "bucket_one" 这个空间拉取 '/' 目录下面所有的文件, 访问域名为 techs.upyun.com。 然后保存到 bucket_two 的 "/bucket_one" 目录中去, 那我就需要填写如下参数

```python
# ----------待拉取的服务名操作员信息-------------
origin_bucket = 'buckeet_one'  # (必填) 待拉取的服务名
origin_username = 'username'  # (必填) 待拉取的服务名下授权的操作员名
origin_password = 'password'  # (必填) 待拉取服务名下授权操作员的密码
host = 'http://techs.upyun.com'  # (必填)  待拉取的服务名的访问域名, 请使用 http// 或者 https:// 开头, 比如 'http://techs.upyun.com'
origin_path = '/'  # (必填) 待拉取的资源路径 (默认会拉取根目录下面的所有目录的文件)
# --------------------------------------------

# ----------目标迁移服务名, 操作员信息-------------
target_bucket = 'bucket_two'  # (必填) 文件迁移的目标服务名
target_username = 'username'  # (必填) 文件迁移的目标服务名的授权操作员名
target_password = 'password'  # (必填) 文件迁移的目标服务名的授权操作员的密码
save_as_prefix = '/bucket_one'  # (选填) 目标服务名的保存路径的前置路径 (如果不填写, 默认迁移后的路径和原路径相同)
# --------------------------------------------
```



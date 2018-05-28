## 使用说明


<pre><code>
$upyun = new upyun("bucket", "user", "password", false);
$upyun->delfile("del.txt"); 


</code></pre>

bucket : 服务名  
user : 操作员账号  
pass : 操作员密码  
false : 是否进行异步删除，如果要进行异步删除则更改为  true  
del.txt : 需要删除的文件URI列表，一行一条URI

* 运行脚本生成的 delsucc.txt 代表删除成功的文件，delfail.txt 代表删除失败的文件。

动态加载文件，访问数据库，获取数据，通过邮件发送出去。
1、sendMail.py文件添加实际的邮件服务器地址
2、sql文件夹中添加需要执行的sql脚本
3、dynamic_module为需要动态导入自定义的模块，或需要动态加入的功能。
4、在conf/module.json文件添加配置，添加需要导入的模块名（dynamic_module.inventory）
和动态模块中需要运行的函数名。
5、inventory.py需要添加实际数据库地址，收件人列表字符串，运行的sql脚本路径。
# bilibili_top_100
服务器(Ubuntu环境下)通过邮件定时发送b站top100视频信息到邮箱

1. 在需要执行的python文件前加上

   #!/usr/bin/python3.6
  
   上面这行的作用是说明使用那个解释器来执行该文件，如果不知道python解释器在哪，可以使用命令which python来查看

2. 给该文件添加可执行的权限 

   chmod  777  test.py
  
　 注意：在脚本文件中如果涉及文件操作，请使用绝对路径
 
3. 添加计划任务

　 crontab -e

　 在文件中追加一行，*/2 * * * * /usr/bin/python3.6 /home/ububtu/test.py
   
   参数意义请参考(https://blog.csdn.net/qq_29980371/article/details/78490367)
   
   保存退出，:wq
   
4. 重启cron服务

　 service cron restart

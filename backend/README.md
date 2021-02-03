为了提高开发效率，搭建好了一个基于flask的后台脚手架工具。  


主要涉及技术： 
    Python3, Flask,Flask-blueprint, Celery, Redis, Sqlalchemy, Restful-Api, Ansible

#部署方法  
1. 安装依赖
> ./up init

2. 配置数据
> 持贝conf.py.default为conf.py, 自行相关db配置

3. 启动服务
>./up restart #：生产环境  
./up dev  #:开发环境  

4. 运行celery worker  
>./up worker  

5. 运行celery beat  
>./up beat




此为EyeOps的后端部署说明文件, 基于python2.7开发

主要涉及技术： 
    Python, Flask,Flask-blueprint, Celery, Redis, Sqlalchemy, Restful-Api, Ansible

#部署方法  

1、建议先安装virtualenv  

2、安装mysql和python相关
yum install mysql-devel python-devel  
使用douban源

3、安装程序依赖
pip install -r requirements.txt
豆瓣源：pip install -r requirements.txt -i http://pypi.douban.com/simple

4、持贝conf.py.default为conf.py,自行修改相关配置

5、运行flask进程
python run.py

6、运行celery进程
celery -A xnops_work.app worker -P gevent -c 100 --loglevel=info
后端运行：
nohup celery worker -A celery_worker.celery --loglevel=info >>/var/log/celery.log &

线上部署：使用nginx+uwsgi
uwsgi运行方式：
参考restart_uwsgi.sh

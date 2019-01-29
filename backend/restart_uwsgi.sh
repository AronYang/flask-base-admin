
# uwsgi control  
pgrep -f 4032|xargs kill -9 &>/dev/null
sleep 2
echo restart uwsgi
uwsgi --socket 127.0.0.1:4032 --wsgi-file run.py --callable app --processes 4 --threads 8 --daemonize /var/log/uwsgi4032.log


# celery control  
pgrep -f celery |xargs kill -9 &>/dev/null  
sleep 1
echo restart celery

export PYTHONOPTIMIZE=1
#解决celery与ansible冲突问题
nohup celery worker -A celery_worker.celery --loglevel=info >>/var/log/celery.log &


# coding=utf-8
import datetime
# from app.tasks import run
from app.tasks import run


def crontab(app):
    '''
    这是定时任务， 在app.factory.fac_app里进行了初始化。
    后续的所有任务，只需要加在这里就可以了。
    说明： func: 冒号前为文件路径，后为文件中的方法
          id: 唯一值，
          trigger: 触发方式，
          seconds: 触发间隔，这里可改为seconds,minutes, hours, days, 等等
    '''
    minuteLate = (datetime.datetime.now() + datetime.timedelta(minutes=1))
    run_time = minuteLate.strftime("%Y-%m-%d %H:%M:%S")
    # jobs = [
    #     {'func': 'app.tasks.run', 'args': ("ansible_tes.hello"),
    #      'id': 'sync_all_routers', 'trigger': 'interval', 'seconds': 3},
    #     # {'func': 'app.crontab.sync_zk:sync_all_routers', 'id': 'sync_all_routers', 'trigger': 'interval', 'minutes': 5},

    #     # {'func': 'app.crontab.sync_zk:sync_all_nodes_and_links',
    #     #     'id': 'sync_all_nodes_and_links', 'trigger': 'interval', 'minutes': 15},

    #     # {'func': 'app.crontab.sync_zk:sync_node_stats',
    #     #     'id': 'sync_node_stats', 'trigger': 'interval', 'minutes': 1},
    #     # {'func': 'app.crontab.sync_zk:watch_router_children',
    #     #     'id': 'watch_router_children', 'trigger': 'date', 'run_date': run_time},

    #     # {'func': 'app.crontab.sync_zk:test2', 'id': 'test2', 'trigger': 'interval', 'seconds': 3},
    # ]
    jobs = [
        {'func': 'app.tasks:delay', 'args': ('ansible_tes:hello',), 'kwargs': {'args': 'heihei args'},
         'trigger': "interval", 'id': "123", 'seconds': 3}

    ]

    for job in jobs:
        app.apscheduler.add_job(**job)

        # app.apscheduler.add_job(func=job, id=job, trigger='interval', seconds=3)

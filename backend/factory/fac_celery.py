# coding=utf-8
from celery import Celery
# from conf import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from celery import platforms  # 如果你不是linux的root用户，这两行没必要
platforms.C_FORCE_ROOT = True  # 允许root权限运行celery


def create_celery(application=None):
    if not application:
        from factory.fac_app import create_app
        application = create_app()
    celery = Celery(application.import_name,
                    broker=application.config['CELERY_BROKER_URL'])
    celery.conf.update(application.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with application.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

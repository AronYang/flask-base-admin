# coding=utf-8

from flask import Flask, jsonify, current_app, request
import os
from conf import Config
from flask_cache import Cache
from flask_apscheduler import APScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from app.views import router
from werkzeug.exceptions import HTTPException, default_exceptions, InternalServerError


def create_app():
    app = Flask(__name__,)
    # app.logger.setLevel(logging.ERROR)
    app.secret_key = 'hello, morning.'
    app.config.from_object(Config)
    return app


def error_handler(error):
    if not isinstance(error, HTTPException):
        error = InternalServerError()
    current_app.logger.error(f"'error {error.code}: [{str(error.description)}:{request.url}]'")

    if isinstance(error.description, dict):
        return error.description, error.code

    return jsonify({"msg": error.description, "status": False}), error.code


def log_handler(app):
    # 日志系统配置
    logfile = app.config['LOG_FILE']
    handler = logging.FileHandler(f'{logfile}', encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    return handler


def init_app():
    from app.crontab import crontab

    app = create_app()

    print(app.config)

    app.logger.addHandler(log_handler(app))
    app.cache = Cache(app)
    app.register_blueprint(router, url_prefix='/api')

    for code in default_exceptions:
        app.register_error_handler(code, error_handler)

    if app.debug or os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        scheduler = APScheduler()
        scheduler.init_app(app)
        crontab(app)
        scheduler.start()
    return app

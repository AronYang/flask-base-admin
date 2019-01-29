# coding=utf-8

from flask import Flask, jsonify, current_app, request
import conf
import os
from flask_cache import Cache
from flask_apscheduler import APScheduler
from app.crontab import crontab
import logging
from app.views import router
from werkzeug.exceptions import HTTPException, default_exceptions, InternalServerError


def error_handler(error):
    if not isinstance(error, HTTPException):
        error = InternalServerError()
    current_app.logger.error(f"'error {error.code}: [{str(error.description)}:{request.url}]'")

    if isinstance(error.description, dict):
        return error.description, error.code

    return jsonify({"msg": error.description, "status": False}), error.code


def log_handler():
    # 日志系统配置
    handler = logging.FileHandler('/var/log/satop.log', encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    return handler


def create_app():
    app = Flask(__name__,)
    app.logger.addHandler(log_handler())
    # app.logger.setLevel(logging.ERROR)
    app.secret_key = 'hello, morning~'
    app.config.from_object(conf)
    app.cache = Cache(app)

    for code in default_exceptions:
        app.register_error_handler(code, error_handler)

    # print 'app.debug:', app.debug, os.environ.get('WERKZEUG_RUN_MAIN')
    if app.debug or os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        scheduler = APScheduler()
        scheduler.init_app(app)
        crontab(app)
        scheduler.start()
    app.register_blueprint(router, url_prefix='/api')
    return app

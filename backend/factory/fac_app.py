# coding=utf-8

from flask import Flask, jsonify, current_app, request
import conf
import os
from flask_cache import Cache
import logging
from app import api
from werkzeug.exceptions import HTTPException, default_exceptions, InternalServerError
from flask_sqlalchemy import SQLAlchemy
from app.models.base import db
from flask_migrate import Migrate


def init_database(app):
    db.init_app(app)
    db.app = app
    Migrate(app, db)


def init_logger(app):
    #: 初始化日志
    log_path = os.path.join(app.config['LOG_DIR'], 'app.log')
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    if app.debug:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)


def init_config(app):
    app.config.from_object(conf)
    if not app.config.get('LOG_DIR'):
        app.config['LOG_DIR'] = app.root_path


def init_route(app):
    app.register_blueprint(api.router, url_prefix='/api')


def init_cache(app):
    app.cache = Cache(app)


def init_error(app):

    def error_handler(error):
        if not isinstance(error, HTTPException):
            error = InternalServerError()
        app.logger.error(f"'error {error.code}: [{str(error.description)}:{request.url}]'")

        if isinstance(error.description, dict):
            return error.description, error.code

        return jsonify({"msg": error.description, "status": False}), error.code

    for code in default_exceptions:
        app.register_error_handler(code, error_handler)


def create_app():
    app = Flask(__name__,)
    init_config(app)
    init_database(app)
    init_logger(app)
    init_route(app)
    init_error(app)
    return app

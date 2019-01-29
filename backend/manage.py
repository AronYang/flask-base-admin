#!/usr/bin/env python
# coding=utf-8
# PYTHON_ARGCOMPLETE_OK

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean, Shell
from factory.fac_app import create_app
from flask_migrate import Migrate, MigrateCommand
from sql_config import db_session, Base
from flask import abort, jsonify
from app import tasks
app = create_app()
manager = Manager(app)
db = Base()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(tasks=tasks)

manager.add_command("runservernoreload", Server(use_reloader=False))
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command('db', MigrateCommand)

# 重写runserver方法，指定默认端口
manager.add_command('runserver', Server(host='0.0.0.0', port=4001, use_debugger=True))


@app.route('/test')
def test():
    app.logger.info('what wrong.')
    abort(406)
    abort(404)
    return 'success'


# @app.errorhandler(404)
# def error_404(error):
#     """这个handler可以catch住所有abort(404)以及找不到对应router的处理请求"""
#     response = dict(status=0, message="Resource Not Found")
#     return jsonify(response), 404


# @app.errorhandler(406)
# def MyErrorHandle(error):
#     response = dict(status=0, message="400 Error, args not allow.")
#     return jsonify(response), 400

if __name__ == "__main__":
    manager.run()

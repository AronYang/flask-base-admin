#!/usr/bin/env python
# coding=utf-8
# PYTHON_ARGCOMPLETE_OK
import click
from flask.cli import FlaskGroup
from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean, Shell
from factory.fac_app import init_app
from flask_migrate import Migrate, MigrateCommand
from app.models.base import db, Base
from flask import abort, jsonify
from app import tasks
app = init_app()
print('manage', app.config.__dict__)

manager = Manager(app)
db_base = Base()
migrate = Migrate(app, db_base)


@app.shell_context_processor
def make_shell_context():
    return dict(tasks=tasks)


manager.add_command("runservernoreload", Server(use_reloader=False))
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command('db', MigrateCommand)

# 重写runserver方法，指定默认端口
# manager.add_command('run', Server(host='0.0.0.0', port=4001))


@manager.command
def run(name='dev'):
    ''''dev' or 'pro', default running for dev.  
    '''
    if name == 'dev':
        app.run(host=app.config['HOST'], port=app.config['PORT'])
    elif name == 'pro':
        pass

# @manager.command('recreate_db', help='Recreates a local database, You probably should not use this on production.')
# def recreate_db():
#     db.drop_all()
#     db.create_all()
#     db.session.commit()


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

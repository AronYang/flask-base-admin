#!/usr/bin/env python
# coding=utf-8
# PYTHON_ARGCOMPLETE_OK
import warnings
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)
import os
from glob import glob
from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean, Shell
from factory.fac_app import create_app
from flask_migrate import MigrateCommand
from flask import abort, jsonify
import subprocess
from app import tasks
from app import models
app = create_app()
manager = Manager(app)
pidfile_path = os.path.join(app.root_path, os.pardir, '.'.join([app.config['NAME'], "pid"]))


@app.shell_context_processor
def make_shell_context():
    model_list = [
        tasks,
        models.users.user.User,
    ]
    model_dict = {}
    for model_obj in model_list:
        model_dict[model_obj.__name__] = model_obj

    return model_dict

manager.add_command("runservernoreload", Server(use_reloader=False))
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))

# 重写runserver方法，指定默认端口
manager.add_command('runserver', Server(host='0.0.0.0', port=4001, use_debugger=True))


@manager.command
def kill():
    '''kill current service'''
    if not os.path.exists(pidfile_path):
        print('Unfound Pid File. ')
        return
    with open(pidfile_path) as f:
        pid = f.read().strip()
        cmd = f'kill -9 {pid}'
        status = subprocess.call(cmd, shell=True)
        if status == 0:
            print(f'Pid is {pid}, Stop successful.')
            os.remove(pidfile_path)


@manager.command
def prod():
    '''Start service by gunicorn, multi works and daemon.'''
    from conf import LOG_DIR
    if not LOG_DIR:
        LOG_DIR = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'logs'
            )
        )
    access_logfile_path = os.path.join(LOG_DIR, 'access.log')
    error_logfile_path = os.path.join(LOG_DIR, 'error.log')

    print('Gunicorn works: %s' % app.config['WORKS'])
    print('Access file: %s' % access_logfile_path)
    print('Error file: %s' % error_logfile_path)
    print('Pid file: %s' % pidfile_path)
    print('Listenning: %s:%s' % (app.config["HOST"], app.config["PORT"]))
    cmd = ' '.join([
        'gunicorn manage:app --worker-class gevent --max-requests 10000 '
        '--limit-request-line 0 --limit-request-field_size 0',
        f'--name {app.config["NAME"]}',
        '--daemon',
        f'--workers {app.config["WORKS"]}',
        f'--access-logfile {access_logfile_path}',
        f'--error-logfile {error_logfile_path}',
        f'--pid {pidfile_path}',
        f'--log-level {"debug" if app.config["DEBUG"] else "info"}',
        '--bind', '{host}:{port} '.format(
            host=app.config["HOST"],
            port=app.config["PORT"],
        )
    ])
    os.system(cmd)


# @click.command()
# @click.option('-f', '--fix-imports', default=False, is_flag=True,
#               help='Fix imports using isort, before linting')

@manager.command
# @manager.option('-f', '--fix_imports', dest='fix_imports', help='fix code', default=False)
def lint(fix_imports=False):
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements', 'venv', 'migrations', '__pycache__', 'logs']
    root_files = glob('*.py')
    root_directories = [
        name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip]
    print('fix_imports', fix_imports)

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        info = '{}: {}'.format(description, ' '.join(command_line))
        print(info)
        # click.echo()
        rv = subprocess.call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


@app.route('/test')
def test():
    app.logger.info('what wrong.')
    from app.common.log import Log
    log = Log('test').logger
    log.info('this is test....')
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

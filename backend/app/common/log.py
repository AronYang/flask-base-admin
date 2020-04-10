import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


def Log(name):
    from conf import LOG_DIR
    if not LOG_DIR:
        LOG_DIR = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir,
                'logs'
            )
        )
    filename = os.path.join(LOG_DIR, f'{name}.log')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 添加TimedRotatingFileHandler
    # 定义一个1秒换一次log文件的handler
    # 保留3个旧log文件
    rf_handler = logging.handlers.TimedRotatingFileHandler(filename=filename, when='D', interval=1,
                                                           backupCount=7)
    rf_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    # 在控制台打印日志
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(handler)
    return logger

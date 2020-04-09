
__all__ = ['Test']
from app.common.log import Log


class Test:
    NGINX = '123456'

    def hello(self, good):
        print('hello', good)


def hello():
    print(' I love you ...')
    log = Log('test')
    log.info('test....')

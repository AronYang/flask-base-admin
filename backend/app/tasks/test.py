
__all__ = ['test']
from app.common.log import Log


class test:
    NGINX = '123456'

    def hello(self, good):
        print('hello', good)


def hello():
    print(' I love you ...')
    log = Log('test')
    log.info('test....')

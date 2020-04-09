#: coding=utf-8
#: function: tasks文件，主要用来存放异步任务
from factory.fac_app import create_app
from factory.fac_celery import create_celery
from importlib import import_module
from inspect import isfunction, isclass
celery = create_celery(create_app())

import inspect
import functools
from celery.schedules import crontab
from app.tasks.cron import Cron


class Inspect:
    """
    ``inspect_mate`` provides more methods to get information about class attribute
    than the standard library ``inspect``.
    This module is Python2/3 compatible, tested under Py2.7, 3.3, 3.4, 3.5, 3.6.
    Includes tester function to check:
    - is regular attribute
    - is property style method
    - is regular method, example: ``def method(self, *args, **kwargs)``
    - is static method
    - is class method
    These are 5-kind class attributes.
    and getter function to get each kind of class attributes of a class.
    """

    @staticmethod
    def is_attribute(klass, attr, value=None):
        """Test if a value of a class is attribute. (Not a @property style
        attribute)
        :param klass: the class
        :param attr: attribute name
        :param value: attribute value
        """
        if value is None:
            value = getattr(klass, attr)
        assert getattr(klass, attr) == value

        if not inspect.isroutine(value):
            if not isinstance(value, property):
                return True
        return False

    @staticmethod
    def is_property_method(klass, attr, value=None):
        """Test if a value of a class is @property style attribute.
        :param klass: the class
        :param attr: attribute name
        :param value: attribute value
        """
        if value is None:
            value = getattr(klass, attr)
        assert getattr(klass, attr) == value

        if not inspect.isroutine(value):
            if isinstance(value, property):
                return True
        return False

    @staticmethod
    def is_regular_method(klass, attr, value=None):
        """Test if a value of a class is regular method.
        example::
            class MyClass(object):
                def to_dict(self):
                    ...
        :param klass: the class
        :param attr: attribute name
        :param value: attribute value
        """
        if value is None:
            value = getattr(klass, attr)
        assert getattr(klass, attr) == value

        if inspect.isroutine(value):
            if not Inspect.is_static_method(klass, attr, value) \
                    and not Inspect.is_class_method(klass, attr, value):
                return True

        return False

    @staticmethod
    def is_static_method(klass, attr, value=None):
        """Test if a value of a class is static method.
        example::
            class MyClass(object):
                @staticmethod
                def method():
                    ...
        :param klass: the class
        :param attr: attribute name
        :param value: attribute value
        """
        if value is None:
            value = getattr(klass, attr)
        assert getattr(klass, attr) == value

        for cls in inspect.getmro(klass):
            if inspect.isroutine(value):
                if attr in cls.__dict__:
                    binded_value = cls.__dict__[attr]
                    if isinstance(binded_value, staticmethod):
                        return True
        return False

    @staticmethod
    def is_class_method(klass, attr, value=None):
        """Test if a value of a class is class method.
        example::
            class MyClass(object):
                @classmethod
                def method(cls):
                    ...
        :param klass: the class
        :param attr: attribute name
        :param value: attribute value
        """
        if value is None:
            value = getattr(klass, attr)
        assert getattr(klass, attr) == value

        for cls in inspect.getmro(klass):
            if inspect.isroutine(value):
                if attr in cls.__dict__:
                    binded_value = cls.__dict__[attr]
                    if isinstance(binded_value, classmethod):
                        return True
        return False


@celery.task(bind=True)
def run(self, filename, method, *args, **kwargs):
    #: imp_first tasks下的文件名称
    #： imp_first 为文件中的类名或方法名
    #： imp_second 为类中的方法名
    if self.request.id:
        '这里可以对tasks的结果进行记录了。'
        print(f'Receive task: {imp_module}')
        print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
            self.request))
    # module_list = imp_module.split('.')
    module_list = [filename, filename.capitalize(), method]
    if len(module_list) >= 2:
        imp_first = module_list[0]
        imp_second = module_list[1]
        if len(module_list) >= 3:
            imp_third = module_list[2]
        else:
            imp_third = None
    else:
        raise Exception('module path error. ')

    imp_first = import_module('app.tasks.' + imp_first)
    imp_second = getattr(imp_first, imp_second)

    if isclass(imp_second):
        #：如果第三个参数是类的属性，则直接返回值。
        if Inspect.is_attribute(imp_second, imp_third):
            return getattr(imp_second(), imp_third)

        #： 如果第三个参数是类方法，则无需实例化类
        elif Inspect.is_class_method(imp_second, imp_third):
            imp_method = getattr(imp_second, imp_third)
            return imp_method(*args, **kwargs)

        #： 如果第三个参数是静态方法，则无需实例化类
        elif Inspect.is_static_method(imp_second, imp_third):
            imp_method = getattr(imp_second, imp_third)
            return imp_method(*args, **kwargs)

        #：如果第三个参数是property类型，则无需给方法加括号
        elif Inspect.is_property_method(imp_second, imp_third):
            return getattr(imp_second(), imp_third)

        #： 普通的类方法
        elif Inspect.is_regular_method(imp_second, imp_third):
            imp_method = getattr(imp_second(), imp_third)
            return imp_method(*args, **kwargs)

    # 如果第二个参数是方法，则直接返回执行的方法。
    if isfunction(imp_second):
        return imp_second(*args, **kwargs)

    raise Exception('task run error. ')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 定时任务。
    sender.add_periodic_task(3, run.s('cron.hello'), name='add every 10')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )

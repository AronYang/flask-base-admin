#: coding=utf-8
#: function: tasks文件，主要用来存放异步任务
from flask import current_app
from factory.fac_app import create_app
from factory.fac_celery import create_celery
from importlib import import_module
import inspect
from app.tasks.inspect_mate import is_attribute, is_class_method, is_property_method, is_regular_method, is_static_method
from inspect import isfunction, isclass
celery = create_celery(current_app)
# from app import celery


@celery.task()
def delay(imp_module, *args, **kwargs):
    run.delay(imp_module, *args, **kwargs)


@celery.task()
def run(imp_module, *args, **kwargs):
    #: imp_first tasks下的文件名称
    #： imp_first 为文件中的类名或方法名
    #： imp_second 为类中的方法名
    module_list = imp_module.split(':')
    print('module_list:', imp_module)
    if len(module_list) >= 2:
        imp_first = module_list[0]
        imp_second = module_list[1]
        if len(module_list) >= 3:
            imp_third = module_list[2]
        else:
            imp_third = None
    else:
        raise Exception('module path error. ')

    print('Receive task: %s.%s.%s' % (imp_first, imp_second, imp_third))

    imp_first = import_module('app.tasks.' + imp_first)
    imp_second = getattr(imp_first, imp_second)

    if isclass(imp_second):
        #：如果第三个参数是类的属性，则直接返回值。
        if is_attribute(imp_second, imp_third):
            return getattr(imp_second(), imp_third)

        #： 如果第三个参数是类方法，则无需实例化类
        elif is_class_method(imp_second, imp_third):
            imp_method = getattr(imp_second, imp_third)
            return imp_method(*args, **kwargs)

        #： 如果第三个参数是静态方法，则无需实例化类
        elif is_static_method(imp_second, imp_third):
            imp_method = getattr(imp_second, imp_third)
            return imp_method(*args, **kwargs)

        #：如果第三个参数是property类型，则无需给方法加括号
        elif is_property_method(imp_second, imp_third):
            return getattr(imp_second(), imp_third)

        #： 普通的类方法
        elif is_regular_method(imp_second, imp_third):
            imp_method = getattr(imp_second(), imp_third)
            return imp_method(*args, **kwargs)

    # 如果第二个参数是方法，则直接返回执行的方法。
    if isfunction(imp_second):
        return imp_second(*args, **kwargs)

    raise Exception('task run error. ')

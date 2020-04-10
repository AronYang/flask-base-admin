# coding=utf-8
import json
import re
import time

import chardet


def Msg(status, msg, object=''):
    # 传入语法  Msg(0,'添加成功')
    Dict = {
        'status': status,  # 成功状态,1为成功，0为失败
        'msg': msg,  # 提示信息
        'result': object,  # 要返回的数据，如果是提示类的则没有返回
    }
    return json.dumps(Dict)


def ipCheck(ip_str):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, ip_str):
        return True
    else:
        return False


def curTime():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time


def convert_encoding(data, new_coding='UTF-8'):
    # 任意字符集转换
    encoding = chardet.detect(data)['encoding']
    if new_coding.upper() != encoding.upper():
        data = data.decode(encoding, data).encode(new_coding)
    return data

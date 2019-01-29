#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author: yangrong
# USAGE:

# 导入创建引擎
from sqlalchemy import create_engine
# 导入会话
import datetime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from conf import db_user, db_passwd, db_port, db_host, db_name

# 数据库连接
engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=utf8' % (db_user, db_passwd, db_host,
                                                                db_port, db_name), pool_recycle=30, pool_size=500, max_overflow=0)

# 会话
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()

Base.query = db_session.query_property()  # 指定model查询调用的会话

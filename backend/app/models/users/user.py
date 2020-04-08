from app.models.base import db, SessionMixin
from sqlalchemy.orm import relationship, backref, joinedload
from passlib.apps import custom_app_context as pwd_context
import datetime


class User(db.Model, SessionMixin):
    __tablename__ = 'u_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)  # 用户名
    name = db.Column(db.String(20))  # 姓名
    sex = db.Column(db.String(2))  # 性别
    phone = db.Column(db.String(64))  # 电话
    mail = db.Column(db.String(64))  # 邮箱
    city = db.Column(db.String(64))  # 城市
    pwd = db.Column(db.String(512))  # 密码，采用sha256加密
    group_id = db.Column(db.Integer)

    create_time = db.Column(db.DateTime, default=datetime.datetime.now,)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 更新时间

    # group = relationship("Group", backref=backref("user"))

    def hash_password(self, password):
        # 加密密码 ，传入明文
        self.pwd = pwd_context.encrypt(password)

    def verify_password(self, password):
        #校验密码 ,传入密文
        return pwd_context.verify(password, self.pwd)

    @classmethod
    def get_username(cls, username):
        return cls.query.filter_by(username=username).first()

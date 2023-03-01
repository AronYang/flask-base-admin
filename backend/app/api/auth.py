# coding=utf8

from flask import Blueprint, Response, current_app, g, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse
from passlib.apps import custom_app_context as pwd_context

from app.models.users.user import User

login = HTTPBasicAuth()
secret_key = 'aron'


@login.error_handler
def auth_error():
    # 默认是返回401，但是401在浏览器端，会自动弹出浏览器带的认证登录界面。影响体验。
    return 'access deny.', 403


@login.verify_password
def verify_password(username_or_token, password):
    '''认证回调'''
    # first try to authenticate by token
    return True
    # user = check_token(username_or_token)
    # if not user:
    #     user = User.get_username(username_or_token)
    #     if user:
    #         hash_pwd = user.pwd
    #         if not pwd_context.verify(password, hash_pwd):
    #             return False
    # g.user = user
    # return True


def check_token(token):
    '''校验token'''
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    user = current_app.cache.get('userid_%s' % data['id'])
    if not user:
        user = User.query.get(data['id'])
        current_app.cache.set('userid_%s' % data['id'], user)
    return user


def create_token(expiration=14400):
    '''生成token'''
    s = Serializer(secret_key, expires_in=expiration)

    # return s.dumps({'id': g.user.id})
    return s.dumps({'id': 2})


class Token(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=True, location='json')
        self.parser.add_argument('password', required=True, location='json')

    def post(self):
        '''获取token'''
        data = self.parser.parse_args()
        username = data.get('username')
        password = data.get('password')

        if not verify_password(username, password):
            return Response(status=403)
        token = create_token()
        return jsonify({'token': token.decode('ascii')})

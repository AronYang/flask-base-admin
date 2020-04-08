from flask import Blueprint
from flask_restful import Resource, Api
from app.api.auth import Token
router = Blueprint('router', __name__)
api = Api(router)

api.add_resource(Token, '/token')

from flask import Blueprint
from flask_restful import Resource, Api
router = Blueprint('router', __name__)
api = Api(router)
import app.views.auth

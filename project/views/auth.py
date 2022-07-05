from flask_restx import Namespace, Resource
from flask import request

from project.dao import AuthDAO
from project.services import AuthService, UsersService
from project.setup_db import db

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegRegView(Resource):
    def post(self):
        req_json = request.json
        user = UsersService(db.session).create(req_json)
        return f"Добавлен в базу: пользователь - {user.name}", 201


@auth_ns.route('/login')
class AuthView(Resource):

    def post(self):
        return AuthService(db.session).login(request.json)

    def put(self):
        return AuthService(db.session).get_new_tokens(request.json['refresh_token'])


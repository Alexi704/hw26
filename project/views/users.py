from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services import UsersService
from project.setup_db import db

users_ns = Namespace("users")


@users_ns.route("/")
class UsersView(Resource):
    @users_ns.response(200, "OK")
    def get(self):
        """Get all users"""
        return UsersService(db.session).get_all_users()


@users_ns.route("/<int:user_id>")
class UserView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def get(self, user_id: int):
        """Get user by id"""
        try:
            return UsersService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User not found")

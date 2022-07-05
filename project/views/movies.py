from flask_restx import abort, Namespace, Resource
from flask import request

from project.exceptions import ItemNotFound
from project.services import MoviesService
from project.setup_db import db
from project.utils import auth_required

movies_ns = Namespace("movies")


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.response(200, "OK")
    @auth_required
    def get(self):
        """Get all movies"""
        return MoviesService(db.session).get_all_movies()


@movies_ns.route("/<int:movie_id>")
class MovieView(Resource):
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Movie not found")
    @auth_required
    def get(self, movie_id: int):
        """Get movie by id"""
        try:
            return MoviesService(db.session).get_item_by_id(movie_id)
        except ItemNotFound:
            abort(404, message="Movie not found")

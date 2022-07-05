from project.dao.models.base import BaseMixin
from project.setup_db import db


class Movie(BaseMixin, db.Model):
    __tablename__ = "movies"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=False)
    trailer = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"), nullable=False)
    director = db.relationship("Director")

    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), nullable=False)
    genre = db.relationship("Genre")

    def __repr__(self):
        return f"<Movie '{self.name.title()}'>"

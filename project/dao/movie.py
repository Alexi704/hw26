from flask import request
from sqlalchemy import desc
from sqlalchemy.orm.scoping import scoped_session
from project.dao.models import Movie
from project.config import BaseConfig

limit_page = BaseConfig.ITEMS_PER_PAGE


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        # проверка запроса в строке ?status=new
        status = request.args.get('status')
        # проверка запроса в строке ?page=2 (любое число)
        page = request.args.get('page')

        if status == 'new' and page is not None:
            page = int(page)
            return self._db_session.query(Movie).order_by(desc(Movie.year)).limit(limit_page).offset(
                limit_page * (page - 1))

        elif status == 'new':
            return self._db_session.query(Movie).order_by(desc(Movie.year))

        elif page is not None:
            page = int(page)
            return self._db_session.query(Movie).limit(limit_page).offset(limit_page * (page - 1))

        return self._db_session.query(Movie).all()

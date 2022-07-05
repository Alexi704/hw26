from flask import request
from sqlalchemy.orm.scoping import scoped_session
from project.dao.models import Director
from project.config import BaseConfig

limit_page = BaseConfig.ITEMS_PER_PAGE


class DirectorDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Director).filter(Director.id == pk).one_or_none()

    def get_all(self):
        # проверка запроса в строке ?page=2 (любое число)
        page = request.args.get('page')
        if page is not None:
            page = int(page)
            return self._db_session.query(Director).limit(limit_page).offset(limit_page * (page - 1))

        return self._db_session.query(Director).all()

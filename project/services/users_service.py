from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.utils import get_hash_password
from sqlalchemy.orm.scoping import scoped_session


class UsersService(BaseService):

    def __init__(self, session: scoped_session):
        super().__init__(session)

    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def create(self, user_d):
        user_d['password'] = get_hash_password(user_d['password'])
        new_user = UserDAO(self._db_session).create(user_d)
        return new_user

    def update(self, user_d):
        if user_d.get('password') is not None:
            user_d['password'] = get_hash_password(user_d['password'])
        user_update = UserDAO(self._db_session).update(user_d)
        return user_update

    def change_password(self, user_d):
        new_password = user_d.get('new_password')
        old_password = user_d.get('old_password')
        old_password_hash = get_hash_password(old_password)
        user = UserDAO(self._db_session).get_by_id(user_d['id'])
        password_db = user.password

        if old_password_hash == password_db:
            user_d['password'] = get_hash_password(new_password)
            user_update = UserDAO(self._db_session).update(user_d)

            return user_update, print(f"Пароль успешно сменен!")

        return print(f"НЕВЕРНО введен первоначальный пароль!")

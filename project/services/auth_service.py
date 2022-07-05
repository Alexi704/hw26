from flask_restx import abort
from project.dao import AuthDAO
from project.services.base import BaseService
from sqlalchemy.orm.scoping import scoped_session
from project.utils import get_hash_password, generate_tokens, decode_token


class AuthService(BaseService):

    def __init__(self, session: scoped_session):
        super().__init__(session)

    def login(self, data: dict):
        user_data = AuthDAO(self._db_session).get_by_username(data['name'])
        print(user_data)
        if user_data.name is None:
            abort(401, message='... User NOT found ...')

        hashed_password = get_hash_password(data['password'])
        if user_data.password != hashed_password:
            abort(401, message='Invalid credentials (неверны учетные данные: пароль)')

        tokens: dict = generate_tokens(
            {
                'name': data['name'],
            }
        )

        return tokens

    def get_new_tokens(self, refresh_token: str):
        decoded_token = decode_token(refresh_token, refresh_token=True)

        tokens = generate_tokens(
            data={
                'name': decoded_token['name'],
            }
        )

        return tokens

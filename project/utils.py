import json
import hashlib
import base64
from flask import request, current_app
from flask_restx import abort
from project.config import BaseConfig
from datetime import datetime, timedelta
import jwt


def read_json(filename, encoding="utf-8"):
    with open(filename, encoding=encoding) as f:
        return json.load(f)


def get_hash_password(password: str) -> str:
    """ Хешируем пароли """
    hashed_password: bytes = hashlib.pbkdf2_hmac(
        hash_name=BaseConfig.PWD_HASH_NAME,
        password=password.encode('utf-8'),  # Convert the password to bytes
        salt=BaseConfig.PWD_HASH_SALT,
        iterations=BaseConfig.PWD_HASH_ITERATIONS
    )
    return base64.b64encode(hashed_password).decode('utf-8')


def generate_tokens(data: dict) -> dict[str, str]:
    """ Генерируем токены """
    data['exp'] = datetime.utcnow() + timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
    data['refresh_token'] = False

    access_token: str = jwt.encode(
        payload=data,
        key=BaseConfig.SECRET_KEY,
        algorithm=BaseConfig.JWT_ALGORITM
    )

    data['exp'] = datetime.utcnow() + timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
    data['refresh_token'] = True

    refresh_token: str = jwt.encode(
        payload=data,
        key=BaseConfig.SECRET_KEY,
        algorithm=BaseConfig.JWT_ALGORITM
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def get_token_from_headers(headers: dict):
    """ Получаем заголовок с токеном из запроса. """
    if 'Authorization' not in headers:
        abort(401)

    return headers['Authorization'].split(' ')[-1]


def decode_token(token: str, refresh_token: bool=False):
    """ Раскодируем токен """
    decoded_token = {}
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=BaseConfig.SECRET_KEY,
            algorithms=[BaseConfig.JWT_ALGORITM],
        )
    except jwt.PyJWTError:
        current_app.logger.info('Got wrong token: "%s"', token)
        abort(401)

    # Проверяем то, что это не refresh_token
    if decoded_token['refresh_token'] != refresh_token:
        abort(400, message='Got wrong token type (это не refresh_token)')

    return decoded_token


def auth_required(func):
    def wrapper(*args, **kwargs):

        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Раскодируем токен
        decoded_token = decode_token(token)

        # Проверяем, что пользователь существует
        if not decoded_token['name']:
            abort(401)

        return func(*args, **kwargs)
    return wrapper


def admin_access_required(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Раскодируем токен
        decoded_token = decode_token(token)

        # Проверяем роль администратор/юзер
        # if decoded_token['role'] != 'admin':
        #     abort(403)

        # Проверяем, что пользователь существует
        if not decoded_token['name']:
            abort(401)

        return func(*args, **kwargs)

    return wrapper
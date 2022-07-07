import base64
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = "Oh!:->it'S_VerY(VERY)_Secret=Key)"
    JSON_AS_ASCII = False

    ITEMS_PER_PAGE = 12

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRE_MINUTES = 30
    TOKEN_EXPIRE_DAYS = 130

    JWT_ALGORITM: str = 'HS256'
    PWD_HASH_NAME = 'sha256'
    PWD_HASH_SALT = base64.b64decode("A-pinch-OF-sAlt!")
    PWD_HASH_ITERATIONS = 100_000


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.dirname(BASEDIR), "project.db")
    # SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_password@db/db_name'

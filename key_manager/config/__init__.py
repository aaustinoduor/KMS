import os
import tempfile
from enum import StrEnum


class Env(StrEnum):
    DEV = "Development"
    PROD = "Production"
    TEST = "Testing"


class BaseConfig:
    """"""
    PORT = 5000
    DEBUG = False
    TESTING = False
    HOST = "127.0.0.1"
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "64d11e0cbd5cd4669ad48db094d94292528fddfb4111745fadfe08b62003a9b4"


class DevConfig(BaseConfig):
    """"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(tempfile.gettempdir(), "key_manager.db")}"


class ProdConfig(BaseConfig):
    """"""
    HOST = "0.0.0.0"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://cowanweks:ultimate@localhost/key_manager"


class TestConfig(BaseConfig):
    """"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

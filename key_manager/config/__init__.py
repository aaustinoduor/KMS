import shutil
import logging
from enum import StrEnum

logger = logging.getLogger('waitress')


class Env(StrEnum):
    DEV = "Development"
    PROD = "Production"
    TEST = "Testing"


class BaseConfig:
    """"""
    PORT = 3000
    DEBUG = False
    TESTING = False
    HOST = "127.0.0.1"
    SESSION_TYPE = "cachelib"
    NPM_BIN_PATH = shutil.which("npm") or exit(-1)
    logger.setLevel(logging.INFO)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "64d11e0cbd5cd4669ad48db094d94292528fddfb4111745fadfe08b62003a9b4"


class DevConfig(BaseConfig):
    """"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/key_manager.db"


class ProdConfig(BaseConfig):
    """"""
    HOST = "0.0.0.0"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://cowanweks:ultimate@localhost/key_manager"


class TestConfig(BaseConfig):
    """"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

import pytest
from flask import Flask
from key_manager import create_app
from key_manager.config import TestConfig


@pytest.fixture()
def app():
    """Flask application instance"""
    yield create_app(TestConfig())


@pytest.fixture()
def client(app: Flask):
    """Flask's testing client"""
    return app.test_client()


@pytest.fixture()
def runner(app: Flask):
    """Flask CLI Runner"""
    return app.test_cli_runner()
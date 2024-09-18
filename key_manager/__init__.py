import os
from flask import Flask
from key_manager.db import models
from key_manager.config import BaseConfig
from key_manager.commands import user_cmd
from key_manager.routes import index, auth
from dotenv import find_dotenv, load_dotenv
from key_manager.extensions import flask_db, fc, fv, fm, fs

load_dotenv(find_dotenv())


def create_app(app_config: BaseConfig):
    """"""
    app = Flask(__name__,
                static_folder=os.path.join(os.getcwd(), "static"))

    # Set Environment Config
    app.config.from_object(app_config)

    # Init Flask Extensions
    fc.init_app(app)
    fv.init_app(app)
    fs.init_app(app)
    flask_db.init_app(app)
    fm.init_app(app, flask_db)

    # Register Blueprints
    app.register_blueprint(auth.auth_route)
    app.register_blueprint(index.index_route)

    # Register Commands
    app.cli.add_command(user_cmd.user_cli)

    # Set Up Logger

    with app.app_context():
        flask_db.create_all()

    return app

from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

from key_manager.routes import user, auth, department, index, staff, role
from key_manager.db import models
from marshmallow import ValidationError
from key_manager.config import BaseConfig
from key_manager.commands import user_cmd
from key_manager.extensions import flask_db, fc, fm, fs, ma
from key_manager.errors_handlers import (handle_bad_request, handle_not_found_request,
                                         handle_internal_server_error_request, handle_validation_error,
                                         handle_database_error)


def create_app(app_config: BaseConfig):
    """"""
    app = Flask(__name__)

    # Set Environment Config
    app.config.from_object(app_config)

    # Init Flask Extensions
    fc.init_app(app)
    fs.init_app(app)
    flask_db.init_app(app)
    ma.init_app(app)
    fm.init_app(app, flask_db)

    # Register Blueprints
    app.register_blueprint(role.role_route)
    app.register_blueprint(auth.auth_route)
    app.register_blueprint(index.index_route)
    app.register_blueprint(user.user_route)
    app.register_blueprint(staff.staff_route)
    app.register_blueprint(department.department_route)

    # Register Commands
    app.cli.add_command(user_cmd.user_cli)

    # Register Error handlers
    with app.app_context():
        # Register Error Handlers
        app.register_error_handler(SQLAlchemyError, handle_database_error)
        app.register_error_handler(400, handle_bad_request)
        app.register_error_handler(ValidationError, handle_validation_error)
        app.register_error_handler(404, handle_not_found_request)
        app.register_error_handler(500, handle_internal_server_error_request)

    # Set Up Logger

    with app.app_context():
        flask_db.create_all()

    return app

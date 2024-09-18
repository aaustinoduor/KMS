import click
from flask import current_app
from key_manager.db.models import User
from sqlalchemy.exc import IntegrityError
from key_manager.utils import hash_password
from key_manager.extensions import flask_db
from flask.cli import AppGroup, with_appcontext

user_cli = AppGroup("user", help="Run user related commands")


@user_cli.command('add')
@click.argument("username")
@click.argument("password")
@with_appcontext
def add(username: str, password: str):
    """Load database with bootstrap data."""
    with current_app.app_context():

        try:
            user = User(username=username, password=hash_password(password))
            flask_db.session.add(user)
            flask_db.session.commit()

        except IntegrityError:
            return click.echo("User already exists!")

        return click.echo(f"Successfully Added {username} as a user!")

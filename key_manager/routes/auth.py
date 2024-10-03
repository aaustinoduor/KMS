from flask import Blueprint, jsonify, request

from key_manager.db.models import User
from key_manager.utils import check_password
from key_manager.schemas.credential import SignInSchema

auth_route = Blueprint("auth_route", __name__, url_prefix="/auth")
signin_schema = SignInSchema()


@auth_route.post("/signin")
def signin():
    """"""

    if not request.is_json:
        return jsonify(msg="Request body must be json!"), 400

    credentials = signin_schema.load(request.json)
    user = User.query.filter_by(username=credentials.username).first()

    if user and check_password(user.password, credentials.password):
        return jsonify(msg=f"Successfully signed in as {credentials.username}!", success=True)

    return jsonify(msg="Wrong username or password! Please check your credentials and try again.", success=False)

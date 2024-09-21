from key_manager.db.models import User
from key_manager.extensions import flask_db
from key_manager.utils import hash_password
from key_manager.db.schemas import UserSchema
from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

user_route = Blueprint("user_route", __name__, url_prefix="/api/users")


@user_route.get("/<string:username>")
def get_user(username: str):
    """"""
    userSchema = UserSchema(exclude=["password"])

    try:
        users = User.query.filter_by(username=username).first()
        serialized_users = userSchema.dump(users)

    except SQLAlchemyError:
        abort(500, jsonify(msg="Database error occurred!", success=False))

    else:
        return jsonify(data=serialized_users, success=True), 201


@user_route.get("/")
def get_users():
    """"""
    userSchema = UserSchema(many=True, exclude=["password"])

    try:
        users = User.query.all()
        serialized_users = userSchema.dump(users)

    except SQLAlchemyError:
        abort(500, jsonify(msg="Database error occurred!", success=False))

    else:
        return jsonify(data=serialized_users, success=True), 201


@user_route.post("/")
def new_user():
    """"""
    userSchema = UserSchema()

    if not request.is_json:
        abort(400, jsonify(msg="Request must be json!", success=False))

    try:
        request_data = userSchema.load(request.json)
        user = User(username=request_data.username, password=hash_password(request_data.password))
        flask_db.session.add(user)

    except IntegrityError:
        print("Error")
        flask_db.session.rollback()
        return jsonify(msg="User already exists!", success=False)

    else:
        flask_db.session.commit()
        return jsonify(msg="User added successfully!", success=True), 201


@user_route.delete("/<string:username>")
def delete_user(username: str):
    """"""
    try:
        user = User.query.filter_by(username=username).first()
        flask_db.session.delete(user)

    except SQLAlchemyError:
        flask_db.session.rollback()
        abort(500,
              jsonify(msg=f"Couldn't delete user {username}! The user may noy exist!", success=False))

    else:
        flask_db.session.commit()
        return jsonify(msg=f"User {username} deleted successfully!", success=True), 200


@user_route.put("/<string:username>")
@user_route.patch("/<string:username>")
def update_user(username: str):
    """"""
    userSchema = UserSchema(exclude=["username"])

    if not request.is_json:
        abort(400, jsonify(msg="Request must be json!", success=False))

    try:
        request_data = userSchema.load(request.json)
        User.query.filter_by(username=username).update({
            "password": hash_password(request_data.password)
        })

    except SQLAlchemyError:
        flask_db.session.rollback()
        abort(400, jsonify(msg="Database error occurred!", success=False))

    else:
        flask_db.session.commit()
        return jsonify(msg="User updated successfully!", success=True), 200

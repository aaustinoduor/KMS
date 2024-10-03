from key_manager.db.models import User
from key_manager.extensions import flask_db
from key_manager.schemas.user import UserSchema, UserCreationSchema, UserUpdateSchema
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

user_route = Blueprint("user_route", __name__, url_prefix="/api/users")


@user_route.get("/<string:user_id>")
def get_user(user_id: str):
    """"""
    userSchema = UserSchema()

    try:
        user = User.query.filter_by(user_id=user_id).first()

        if user is None:
            return jsonify(msg=f"User {user_id} does not exist!")

        serialized_user = userSchema.dump(user)

    except SQLAlchemyError:
        jsonify(msg="Database error occurred!", success=False), 500

    else:
        return jsonify(data=serialized_user, success=True), 200


@user_route.get("")
def get_users():
    """"""
    userSchema = UserSchema(many=True)

    try:
        users = User.query.all()
        serialized_users = userSchema.dump(users)

    except SQLAlchemyError:
        jsonify(msg="Database error occurred!", success=False), 500

    else:
        return jsonify(data=serialized_users, success=True), 200


@user_route.post("")
def new_user():
    """"""
    user_creation_schema = UserCreationSchema()

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        data = request.json
        user = user_creation_schema.load(data)
        flask_db.session.add(user)

    except SQLAlchemyError as ex:
        flask_db.session.rollback()
        return jsonify(msg="User already exists!", success=False), 400

    else:
        flask_db.session.commit()
        return jsonify(msg="User added successfully!", success=True), 201


@user_route.delete("/<string:user_id>")
def delete_user(user_id: str):
    """"""
    try:
        user = User.query.filter_by(user_id=user_id).first()

        if user is None:
            return jsonify(msg=f"User {user_id} does not exist!", success=False)

        flask_db.session.delete(user)

    except SQLAlchemyError:
        flask_db.session.rollback()
        jsonify(msg=f"Couldn't delete user {user_id}!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg=f"User {user_id} deleted successfully!", success=True), 200


@user_route.put("<string:user_id>")
@user_route.patch("<string:user_id>")
def update_user(user_id: str):
    """"""
    user_update_schema = UserUpdateSchema()

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        updated_user = user_update_schema.load(request.json)
        user = User.query.filter_by(user_id=user_id).first()

        if user is None:
            return jsonify(msg=f"Could not update user {user_id}! User does not exist!", success=False)

        user.update(updated_user)

    except SQLAlchemyError:
        flask_db.session.rollback()
        return jsonify(msg=f"Could not update user {user_id}!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg=f"User {user_id} updated successfully!", success=True), 200

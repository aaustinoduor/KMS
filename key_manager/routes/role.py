from key_manager.extensions import flask_db
from flask import Blueprint, jsonify, request
from key_manager.db.models import Role
from key_manager.schemas.role import RoleSchema, RoleCreationSchema, RoleUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

role_route = Blueprint("role_route", __name__, url_prefix="/api/roles")


@role_route.get("/<string:role_id>")
def get_role(role_id: str):
    """"""
    roleSchema = RoleSchema()

    try:
        role = Role.query.filter_by(role_id=role_id).first()

        if role is None:
            return jsonify(msg=f"Role {role_id} does not exist!")

        serialized_role = roleSchema.dump(role)

    except SQLAlchemyError:
        jsonify(msg="Database error occurred!", success=False), 500

    else:
        return jsonify(data=serialized_role, success=True), 200


@role_route.get("")
def get_roles():
    """"""
    role_schema = RoleSchema(many=True)

    try:
        roles = Role.query.all()
        serialized_roles = role_schema.dump(roles)

    except SQLAlchemyError:
        return jsonify(msg="Database error occurred!", success=False), 500

    else:
        return jsonify(data=serialized_roles, success=True), 200


@role_route.post("")
def new_role():
    """"""
    role_creation_schema = RoleCreationSchema()

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        role = role_creation_schema.load(request.json)
        flask_db.session.add(role)
        flask_db.session.commit()

    except IntegrityError as ex:
        flask_db.session.rollback()
        return jsonify(msg="Role already exists!", success=False), 400

    else:
        return jsonify(msg=f"Role {role.role_id} added successfully!", success=True), 201


@role_route.delete("/<string:role_id>")
def delete_role(role_id: str):
    """"""
    try:
        role = Role.query.filter_by(role_id=role_id).first()

        if role is None:
            return jsonify(msg=f"Role {role_id} does not exist!", success=False)

        flask_db.session.delete(role)

    except SQLAlchemyError:
        flask_db.session.rollback()
        jsonify(msg=f"Couldn't delete role {role_id}!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg=f"Role {role_id} deleted successfully!", success=True), 200


@role_route.put("/<string:role_id>")
@role_route.patch("/<string:role_id>")
def update_role(role_id: str):
    """"""
    role_update_schema = RoleUpdateSchema()

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        updated_role = role_update_schema.load(request.json)
        role = Role.query.filter_by(role_id=role_id).first()

        if role is None:
            return jsonify(msg=f"Could not update role {role_id}! Role does not exist!", success=False)

        role.update(updated_role)

    except SQLAlchemyError:
        flask_db.session.rollback()
        return jsonify(msg=f"Could not update {role_id} role!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg=f"Role {role_id} updated successfully!", success=True), 200

from key_manager.extensions import flask_db
from flask import Blueprint, jsonify, request
from key_manager.db.models import Department
from key_manager.schemas.department import DepartmentSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from key_manager.utils import gen_id

department_route = Blueprint("department_route", __name__, url_prefix="/api/departments")


@department_route.get("/<string:department_id>")
def get_department(department_id: str):
    """"""
    departmentSchema = DepartmentSchema()

    try:
        department = Department.query.filter_by(department_id=department_id).first()

        if department is None:
            return jsonify(msg="Department does not exist!")

        serialized_department = departmentSchema.dump(department)

    except SQLAlchemyError:
        jsonify(msg="Database error occurred!", success=False), 500

    else:
        return jsonify(data=serialized_department, success=True), 200


@department_route.get("")
def get_departments():
    """"""
    departmentSchema = DepartmentSchema(many=True)

    try:
        departments = Department.query.all()
        serialized_departments = departmentSchema.dump(departments)

    except SQLAlchemyError:
        jsonify(msg="Database error occurred!", success=False), 500

    else:
        return jsonify(data=serialized_departments, success=True), 200


@department_route.post("")
def new_department():
    """"""
    departmentSchema = DepartmentSchema(exclude=("department_id",))

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        request_data = departmentSchema.load(request.json)
        department_data = departmentSchema.dump(request_data)

        department = Department(department_id=gen_id(), **department_data)

        flask_db.session.add(department)

    except IntegrityError:
        flask_db.session.rollback()
        return jsonify(msg="Department already exists!", success=False), 400

    else:
        flask_db.session.commit()
        return jsonify(msg="Department added successfully!", success=True), 201


@department_route.delete("/<string:department_id>")
def delete_department(department_id: str):
    """"""
    try:
        department = Department.query.filter_by(department_id=department_id).first()

        if department is None:
            return jsonify(msg=f"Department does not exist!", success=False)

        flask_db.session.delete(department)

    except SQLAlchemyError:
        flask_db.session.rollback()
        jsonify(msg=f"Couldn't delete department {department_id}!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg=f"Department {department_id} deleted successfully!", success=True), 200


@department_route.put("/<string:department_id>")
@department_route.patch("/<string:department_id>")
def update_department(department_id: str):
    """"""
    departmentSchema = DepartmentSchema(exclude=("department_id",))

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        updated_department = departmentSchema.dump(departmentSchema.load(request.json))
        
        department = Department.query.filter_by(department_id=department_id).first()

        if department is None:
            return jsonify(msg=f"Could not update department {department_id}! Department does not exist!", success=False)

        # Check and remove items from schema that are not to be updated by user
        updated_department = {key: value for key, value in updated_department.items() if key in request.json}

        department.update(updated_department)

    except SQLAlchemyError as ex:
        print(ex)
        flask_db.session.rollback()
        return jsonify(msg=f"Could not update department {department_id}!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg="Department updated successfully!", success=True), 200

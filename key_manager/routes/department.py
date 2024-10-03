from key_manager.extensions import flask_db
from key_manager.db.models import Department
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from key_manager.schemas.department import DepartmentSchema, DepartmentCreationSchema, DepartmentUpdateSchema

department_route = Blueprint("department_route", __name__, url_prefix="/api/departments")


@department_route.get("/<string:department_id>")
def get_department(department_id: str):
    """"""
    departmentSchema = DepartmentSchema()

    try:
        department = Department.query.filter_by(department_id=department_id).first()

        if department is None:
            return jsonify(msg=f"Department {department_id} does not exist!")

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
    department_creation_Schema = DepartmentCreationSchema()

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        department = department_creation_Schema.load(request.json)
        flask_db.session.add(department)

    except IntegrityError:
        flask_db.session.rollback()
        return jsonify(msg="Department already exists!", success=False), 400

    else:
        flask_db.session.commit()
        return jsonify(msg=f"Department {department.department_id} added successfully!", success=True), 201


@department_route.delete("/<string:department_id>")
def delete_department(department_id: str):
    """"""
    try:
        department = Department.query.filter_by(department_id=department_id).first()

        if department is None:
            return jsonify(msg=f"Department {department_id} does not exist!", success=False)

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
    department_updated_schema = DepartmentUpdateSchema()

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        updated_department = department_updated_schema.load(request.json)
        department = Department.query.filter_by(department_id=department_id).first()

        if department is None:
            return jsonify(msg=f"Could not update department {department_id}! Department does not exist!", success=False)

        department.update(updated_department)

    except SQLAlchemyError as ex:
        print(ex)
        flask_db.session.rollback()
        return jsonify(msg=f"Could not update department {department_id}!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg=f"Department {department_id} updated successfully!", success=True), 200

from key_manager.utils import gen_id
from key_manager.extensions import flask_db
from flask import Blueprint, jsonify, request
from key_manager.db.models import Staff
from key_manager.schemas.staff import StaffSchema, StaffCreationSchema, StaffUpdateSchema
from sqlalchemy.exc import SQLAlchemyError

staff_route = Blueprint("staff_route", __name__, url_prefix="/api/staffs")


@staff_route.get("/<string:staff_no>")
def get_staff(staff_no: str):
    """"""
    staffSchema = StaffSchema()

    try:
        staff = Staff.query.filter_by(staff_no=staff_no).first()

        if staff is None:
            return jsonify(msg="Staff does not exist!")

        serialized_staff = staffSchema.dump(staff)

    except SQLAlchemyError:
        jsonify(msg="Database error occurred!", success=False), 500

    else:
        return jsonify(data=serialized_staff, success=True), 200


@staff_route.get("")
def get_staffs():
    """"""
    staffSchema = StaffSchema(many=True)

    try:
        staffs = Staff.query.all()
        serialized_staffs = staffSchema.dump(staffs)

    except SQLAlchemyError:
        jsonify(msg="Database error occurred!", success=False), 500

    else:
        return jsonify(data=serialized_staffs, success=True), 200


@staff_route.post("")
def new_staff():
    """"""
    staff_creation_schema = StaffCreationSchema()

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        staff = staff_creation_schema.load(request.json)
        flask_db.session.add(staff)

    except SQLAlchemyError:
        flask_db.session.rollback()
        return jsonify(msg="Staff already exists!", success=False), 400

    else:
        flask_db.session.commit()
        return jsonify(msg="Staff added successfully!", success=True), 201


@staff_route.delete("/<string:staff_no>")
def delete_staff(staff_no: str):
    """"""
    try:
        staff = Staff.query.filter_by(staff_no=staff_no).first()

        if staff is None:
            return jsonify(msg=f"Staff does not exist!", success=False)

        flask_db.session.delete(staff)

    except SQLAlchemyError:
        flask_db.session.rollback()
        jsonify(msg=f"Couldn't delete staff {staff_no}!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg=f"Staff {staff_no} deleted successfully!", success=True), 200


@staff_route.put("/")
@staff_route.patch("/")
def update_staff():
    """"""
    staff_update_schema = StaffUpdateSchema()

    if not request.is_json:
        jsonify(msg="Request must be json!", success=False), 400

    try:
        updated_staff = staff_update_schema.dump(staff_update_schema.load(request.json))
        staff_no = updated_staff["staff_no"]
        staff = Staff.query.filter_by(staff_no=staff_no).first()

        if staff is None:
            return jsonify(msg=f"Could not update staff {staff_no}! Staff does not exist!", success=False)

        staff.update(updated_staff)

    except SQLAlchemyError as ex:
        flask_db.session.rollback()
        return jsonify(msg=f"Could not update staff {staff_no}!", success=False), 500

    else:
        flask_db.session.commit()
        return jsonify(msg="Staff updated successfully!", success=True), 200

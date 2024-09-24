import re
from key_manager.db import models
from key_manager.db.models import Staff
from key_manager.extensions import ma
from marshmallow import fields, Schema, validates, ValidationError, post_load, post_dump


class StaffSchema(ma.SQLAlchemyAutoSchema):
    """"""
    user = fields.Nested("UserSchema")
    department = fields.Nested("DepartmentSchema")
    full_name = fields.Method("get_fullname", dump_only=True)

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @post_dump
    def remove_name_fields(self, data, **kwargs):
        data.pop('first_name', None)
        data.pop('last_name', None)
        return data

    class Meta:
        include_fk = True
        model = models.Staff
        load_instance = True
        include_relationships = True
        exclude = ("user_id", "department_id")


class StaffCreationSchema(Schema):
    """"""

    staff_no = fields.String(required=True)
    department_id = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    nat_id = fields.String(required=True)
    photo = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.String(required=True)
    authorised = fields.Boolean(required=True)
    user = fields.Nested("UserCreationSchema")

    @validates("email")
    def validate_email(self, value):
        """Validate user's email"""
        if not re.match("", value):
            raise ValidationError("Invalid email format!")

    @post_load
    def make_staff(self, data, **kwargs):
        """"""
        return Staff(user_id=data["user"].user_id, **data)


class StaffUpdateSchema(Schema):
    """"""
    staff_no = fields.String(required=True)
    department_id = fields.String(required=False)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    nat_id = fields.String(required=False)
    photo = fields.String(required=False)
    phone = fields.String(required=False)
    email = fields.String(required=False)
    authorised = fields.Boolean(required=False)

    @post_load
    def make_staff(self, data, **kwargs):
        """"""
        return data
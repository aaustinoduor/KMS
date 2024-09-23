import re
from key_manager.db import models
from key_manager.db.models import Staff, User
from key_manager.extensions import ma
from marshmallow import fields, Schema, validates, ValidationError, post_load


class StaffSchema(ma.SQLAlchemyAutoSchema):
    """"""
    user = fields.Nested("UserSchema")

    class Meta:
        include_fk = True
        model = models.Staff
        load_instance = True
        include_relationships = True
        exclude = ("user_id", "staff_id")


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
        data["user_id"] = data["user"].user_id
        return Staff(**data)


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
    user = fields.Nested("UserUpdateSchema")

    @post_load
    def make_staff(self, data, **kwargs):
        """"""
        return data
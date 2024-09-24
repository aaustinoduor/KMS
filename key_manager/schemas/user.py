from key_manager.db import models
from bcrypt import gensalt, hashpw
from key_manager.utils import gen_id
from key_manager.db.models import User
from key_manager.extensions import ma
from marshmallow_sqlalchemy import auto_field
from marshmallow import Schema, fields, ValidationError, validates, post_load


class UserSchema(ma.SQLAlchemySchema):
    """"""
    user_id = auto_field()
    username = auto_field()
    twofa_enabled = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    roles = fields.Nested("RoleSchema", dump_only=True)

    class Meta:
        include_fk = True
        model = models.User
        load_instance = True
        include_relationships = True


class UserCreationSchema(Schema):
    """"""

    username = fields.String(required=True)
    password = fields.String(required=True)
    twofa_enabled = fields.Boolean(required=False)

    @validates("username")
    def validates_username(self, value):
        """Validate user's nickname"""
        if len(value) < 3:
            raise ValidationError("Username must be 3 or more characters!")

    @validates("password")
    def validates_password(self, value):
        """Validate user password"""

        if len(value) < 8:
            raise ValidationError("Password length must be 8 or more!")

        if not any(c.isupper() for c in value):
            raise ValidationError("Password must contain an upper case!")

    @post_load
    def make_user(self, data, **kwargs):
        """"""
        # Hash the password if it's present
        if 'password' in data:
            salt = gensalt()
            data['password'] = hashpw(data['password'].encode(), salt).decode()

        return User(user_id=gen_id(), **data)


class UserUpdateSchema(Schema):
    """"""
    username = fields.String(required=True)
    password = fields.String(required=False)
    twofa_enabled = fields.Boolean(required=False)

    @validates("password")
    def validates_password(self, value):
        """Validate user password"""

        if len(value) < 8:
            raise ValidationError("Password length must be 8 or more!")

        if not any(c.isupper() for c in value):
            raise ValidationError("Password must contain an upper case!")

    @post_load
    def make_user(self, data, **kwargs):
        """"""
        # Hash the password if it's present
        if 'password' in data:
            salt = gensalt()
            data['password'] = hashpw(data['password'].encode(), salt).decode()

        return data
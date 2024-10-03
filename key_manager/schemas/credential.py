from key_manager.db.models import User
from marshmallow import Schema, fields, post_load


class SignInSchema(Schema):
    """"""
    username = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def make_creds(self, data, **kwargs):
        return User(**data)

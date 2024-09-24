from slugify import slugify
from key_manager.db import models
from key_manager.utils import gen_id
from key_manager.extensions import ma
from marshmallow import Schema, fields, post_load


class RoleSchema(ma.SQLAlchemyAutoSchema):
    """"""
    class Meta:
        include_fk = True
        model = models.Role
        load_instance = True
        include_relationships = True


class RoleCreationSchema(Schema):
    """"""

    name = fields.String(required=True)
    description = fields.String(required=False)
    permissions = fields.String(required=False)
    access_level = fields.Integer(required=True)
    scope = fields.String(required=False)
    is_active = fields.String(default=True)

    @post_load
    def make_role(self, data, **kwargs):
        """"""
        return models.Role(role_id=gen_id(), slug=slugify(data["name"]), **data)


class RoleUpdateSchema(Schema):
    """"""
    name = fields.String(required=False)
    description = fields.String(required=False)
    permissions = fields.String(required=False)
    access_level = fields.Integer(required=False)
    scope = fields.String(required=False)
    is_active = fields.Boolean(required=False)

    @post_load
    def make_role(self, data, **kwargs):
        """"""
        if 'name' in data:
            name = data["name"]
            slug = slugify(name)
            data["slug"] = slug

        return data
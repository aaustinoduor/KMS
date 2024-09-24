from key_manager.db import models
from key_manager.utils import gen_id
from key_manager.extensions import ma
from marshmallow import fields, Schema, post_load


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    """"""
    class Meta:
        include_fk = True
        model = models.Department
        load_instance = True
        include_relationships = True


class DepartmentCreationSchema(Schema):
    """"""

    name = fields.String(required=True)

    @post_load
    def make_department(self, data, **kwargs):
        """"""
        return models.Department(department_id=gen_id(), **data)


class DepartmentUpdateSchema(Schema):
    """"""
    name = fields.String(required=False)

    @post_load
    def make_department(self, data, **kwargs):
        """"""
        return data
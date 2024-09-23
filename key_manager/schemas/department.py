from key_manager.db import models
from marshmallow import fields
from key_manager.extensions import ma


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    """"""

    class Meta:
        include_fk = True
        model = models.Department
        load_instance = True
        include_relationships = True

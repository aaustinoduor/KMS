import sqlalchemy as sa
from key_manager.db import models
from key_manager.extensions import ma


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = models.User
        load_instance = True
        include_relationships = True
        exclude = ["user_id"]

import datetime as dt
from key_manager.utils import gen_id
from sqlalchemy.orm import mapped_column
from key_manager.extensions import flask_db
from sqlalchemy import DateTime, String, ForeignKey, Column, Table


class BaseModel(flask_db.Model):
    """Base Model"""
    __abstract__ = True

    created_at = mapped_column(DateTime, default=dt.datetime.now())
    updated_at = mapped_column(DateTime, onupdate=dt.datetime.now())

    def save(self):
        """Save the current model instance."""
        flask_db.session.add(self)
        flask_db.session.commit()

    def update(self, data):
        """Update the user instance with the provided data."""
        for key, value in data.items():
            setattr(self, key, value)

    def delete(self):
        """Delete the current model instance."""
        flask_db.session.delete(self)
        flask_db.session.commit()

    @classmethod
    def get_by_id(cls, item_id):
        """Get a model instance by primary key."""
        return cls.query.get(item_id)

    @classmethod
    def all(cls):
        """Return all records of the model."""
        return cls.query.all()


# Association table for many-to-many relationship between users and roles
user_roles = Table('user_roles', BaseModel.metadata,
                   Column('user_role_id', String, default=lambda: gen_id()),
                   Column('user_id', String, ForeignKey('users.user_id')),
                   Column('role_id', String, ForeignKey('roles.role_id'))
                   )
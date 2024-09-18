from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column
from key_manager.extensions import flask_db
import datetime as dt


class BaseModel(flask_db.Model):
    """Base Model"""
    __abstract__ = True

    created_at = mapped_column(DateTime, default=dt.datetime.now())
    updated_at = mapped_column(DateTime, default=dt.datetime.now())
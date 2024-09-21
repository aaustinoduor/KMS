from uuid import uuid4
import datetime as dt
from typing import List
from key_manager.db import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, String, Boolean, ForeignKey, Date, DateTime


class Staff(BaseModel):
    """"""
    __tablename__ = "staffs"

    staff_no = mapped_column(String, primary_key=True)
    department_id = mapped_column(String, unique=False, nullable=False)
    first_name = mapped_column(String, unique=False, nullable=False)
    last_name = mapped_column(String, unique=False, nullable=False)
    nat_id = mapped_column(String, unique=True, nullable=False)
    photo = mapped_column(String, nullable=True)
    email = mapped_column(String, unique=True, nullable=False)
    phone = mapped_column(String, unique=True, nullable=False)
    authorised = mapped_column(Boolean, unique=False, nullable=False, default=False)

    # Relationships
    department: Mapped["Department"] = relationship(backref="staff")


class User(BaseModel):
    """"""
    __tablename__ = "users"

    user_id = mapped_column(String, primary_key=True)
    staff_no = mapped_column(ForeignKey("staffs.staff_no"), unique=True, nullable=False)
    username = mapped_column(String,unique=True, nullable=False)
    password = mapped_column(String, nullable=False)

    def __init__(self, password: str = None, username: str = None):
        self.user_id = uuid4().hex
        self.username = username
        self.password = password


class Department(BaseModel):
    """"""
    __tablename__ = "departments"

    department_id = mapped_column(String, primary_key=True, unique=True)
    name = mapped_column(String, nullable=False)
    keys: Mapped[List["Key"]] = relationship(backref="department")


class Key(BaseModel):
    """"""
    __tablename__ = "keys"

    key_no = mapped_column(String, primary_key=True, nullable=False)
    department_id = mapped_column(String, ForeignKey("departments.department_id"), nullable=False)
    available = mapped_column(Boolean, unique=False, nullable=False, default=True)
    description = mapped_column(String, unique=False, nullable=True)


class Issue(BaseModel):
    """"""
    __tablename__ = "key_issue"

    issue_no = mapped_column(String, primary_key=True)
    key_no = mapped_column(String, ForeignKey("keys.key_no"), nullable=False)
    staff_no = mapped_column(String, ForeignKey("staffs.staff_no"), nullable=False)
    issue_date = mapped_column(DateTime, default=dt.datetime.now())
    return_date = mapped_column(Date, nullable=False)

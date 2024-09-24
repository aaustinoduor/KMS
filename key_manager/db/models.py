import datetime as dt
from typing import List
from key_manager.utils import gen_id
from key_manager.db import BaseModel, user_roles
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from sqlalchemy import Integer, Numeric, String, Boolean, ForeignKey, Date, DateTime


class Role(BaseModel):
    __tablename__ = 'roles'

    role_id = mapped_column(String, primary_key=True, default=lambda: gen_id())
    name = mapped_column(String, nullable=False, unique=True)
    slug = mapped_column(String, nullable=False, unique=True)
    description = mapped_column(String, nullable=True)
    permissions = mapped_column(String, nullable=True)  # Can store as comma-separated values or JSON
    access_level = mapped_column(Integer, nullable=False, default=1)
    scope = mapped_column(String, nullable=True)  # E.g., 'global', 'department-specific'
    is_active = mapped_column(Boolean, default=True)

    users = Relationship('User', secondary=user_roles, back_populates='roles')

    def __repr__(self):
        return f"<Role(name='{self.name}', access_level={self.access_level})>"


class User(BaseModel):
    """"""
    __tablename__ = "users"

    user_id = mapped_column(String, primary_key=True, default=lambda: gen_id())
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    twofa_enabled = mapped_column(Boolean, default=False)

    # Relationships
    staff: Mapped["Staff"] = Relationship(back_populates="user")
    roles = Relationship('Role', secondary=user_roles, back_populates='users')

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Staff(BaseModel):
    """"""
    __tablename__ = "staffs"

    staff_id = mapped_column(String, primary_key=True, default=lambda: gen_id())
    staff_no = mapped_column(String, unique=True, nullable=False)
    user_id = mapped_column(String, ForeignKey("users.user_id"), unique=True, nullable=False)
    department_id = mapped_column(String, ForeignKey("departments.department_id"), nullable=False)
    first_name = mapped_column(String, unique=False, nullable=False)
    last_name = mapped_column(String, unique=False, nullable=False)
    nat_id = mapped_column(String, unique=True, nullable=False)
    photo = mapped_column(String, nullable=True)
    email = mapped_column(String, unique=True, nullable=False)
    phone = mapped_column(String, unique=True, nullable=False)
    authorised = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped["User"] = Relationship(back_populates="staff")
    department: Mapped["Department"] = Relationship(back_populates="staffs")


class Department(BaseModel):
    """"""
    __tablename__ = "departments"

    department_id = mapped_column(String, primary_key=True, default=lambda: gen_id())
    name = mapped_column(String, nullable=False, unique=True)

    # Relationships
    staffs: Mapped[List["Staff"]] = Relationship(back_populates="department")
    keys: Mapped[List["Key"]] = Relationship(backref="department")


class Key(BaseModel):
    """"""
    __tablename__ = "keys"

    key_no = mapped_column(String, primary_key=True, default=lambda: gen_id())
    department_id = mapped_column(String, ForeignKey("departments.department_id"), nullable=False)
    available = mapped_column(Boolean, unique=False, nullable=False, default=True)
    description = mapped_column(String, unique=False, nullable=True)


class Issue(BaseModel):
    """"""
    __tablename__ = "key_issue"

    issue_no = mapped_column(String, primary_key=True, default=lambda: gen_id())
    key_no = mapped_column(String, ForeignKey("keys.key_no"), nullable=False)
    staff_id = mapped_column(String, ForeignKey("staffs.staff_id"), nullable=False)
    issue_date = mapped_column(DateTime, default=dt.datetime.now())
    return_date = mapped_column(Date, nullable=False)

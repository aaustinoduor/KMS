from .db import app, db
from typing import List
from sqlalchemy import Integer, String, Boolean, ForeignKey, TIMESTAMP,DATE
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Staff(db.Model):
    __tablename__ = "staffs"
    staff_no: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    department_id: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    department: Mapped["Department"] = relationship(backref="staff")
    first_name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    national_id_no: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    photo: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    authorised: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False, default=False)

    def serialize(self):
        return {
            "staff_no":self.staff_no,
            "department_id":self.department_id,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "national_id_no":self.national_id_no,
            "photo":self.photo,
            "email":self.email,
            "phone":self.phone,
            "authorised":self.authorised
        }


class User(db.Model):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    staff_no: Mapped[str] = mapped_column(ForeignKey("staffs.staff_no"), unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String,unique=False, nullable=False)
    password: Mapped[str] = mapped_column(String,unique=False, nullable=False)



class Department(db.Model):
    __tablename__ = "departments"
    department_id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    department: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    department_head: Mapped[str] = mapped_column(ForeignKey("staffs.staff_no"), nullable=True)
    keys: Mapped[List["Key"]] = relationship(backref="department")


class Key(db.Model):
    __tablename__ = "keys"
    key_no: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    department_id: Mapped[str] = mapped_column(ForeignKey("departments.department_id"), unique=False, nullable=False)
    available: Mapped[int] = mapped_column(Boolean, unique=False, nullable=False, default=True)
    description: Mapped[str] = mapped_column(String, unique=False, nullable=True)

class Issue(db.Model):
    __tablename__ = "key_issue"
    issue_no: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key_no: Mapped[str] = mapped_column(String,ForeignKey("keys.key_no"), unique=False)
    staff_no: Mapped[str] = mapped_column(String, ForeignKey("staffs.staff_no"))
    issue_date: Mapped[str] = mapped_column(TIMESTAMP(True), unique=False)
    return_date: Mapped[str] = mapped_column(DATE, unique=False)


with app.app_context():
    db.create_all()
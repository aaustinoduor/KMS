from flask import flash, jsonify
from bcrypt import hashpw, gensalt
from .models import app, db, User, Staff, Department, Key,Issue
from .errors import UniqueViolation


# Get handles go below
def get_keys():
    pass

def get_users():
    pass

def get_departments():
    pass

def get_staffs():
    staffs = Staff.query.all()
    return staffs


# post handles go below
def new_key(key: dict):
    new_key = Key(
        key_no=key.keyno,
        department_id=key.departmentid,
        description=key.description
    )

    try:
        db.session.add(new_key)
        db.session.commit()
        return "Key added successfully!"

    except UniqueViolation as e:
        flash("Key already exists!")
        return e.pgerror

def new_user(user: dict):
    salt = gensalt()
    password = f"{user.get('password')}".encode()
    hpassword = hashpw(password, salt)

    new_user = User(staff_no=user.get("staffno"), user_name=user.get("username"), password=hpassword)

    try:
        db.session.add(new_user)
        db.session.commit()
        return "User added successfully!"

    except UniqueViolation as e:
        flash("User already exists!")
        return e.pgerror

def new_department(department: dict):
    new_department = Department(
                    department_id=department.get("departmentid"),
                    department=department.get("department"),
                    department_head=department.get("departmenthead"))
    try:
        db.session.add(new_department)
        db.session.commit()
        return "Department added successfully!"

    except UniqueViolation as e:
        flash("Department already exists!")
        return e.pgerror

def new_staff(staff: dict):
    authorised = False

    if(staff.get("authorised") == 'True') :
        authorised = True
    else:
        authorised = False

    new_staff = Staff(staff_no=staff.get("staffno"),
                       first_name=staff.get("firstname"),
                       last_name=staff.get("lastname"),
                       national_id_no=staff.get("nationalidno"),
                       authorised= authorised, phone=staff.get("phone"),
                       email=staff.get("email"), photo=staff.get("photo"))
    try:

        db.session.add(new_staff)
        db.session.commit()
        return "Staff added successfully!"

    except UniqueViolation as e:
        flash("Staff already exists!")
        return e.pgerror


def give_key(issuance):
    new_issuance = Issue(
                       key_no=issuance.get("keyno"),
                       staff_no=issuance.get("staffno"),
                       return_date=issuance.get("returndate")
                    )
    try:

        db.session.add(new_issuance)
        db.session.commit()
        return "Key  issued successfully!"

    except UniqueViolation as e:
        flash("Key already issued!")
        return e.pgerror

# put handles go below
def update_key():
    pass

def update_user():
    pass

def update_department():
    pass

def update_staff():
    pass

# put handles go below
def delete_key():
    pass

def delete_user():
    pass

def delete_department():
    pass

def delete_staff():
    pass
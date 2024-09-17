from .handlers import app, new_user,new_staff,new_department,new_key, get_staffs, get_users
from flask import Response, render_template, url_for, redirect,request


@app.route("/", methods=["GET"])
def index_route():
    return render_template("index.html")

# TODO guarded route
@app.route("/signup", methods=["POST", "GET"])
def signup_route():
    staffs = get_staffs()
    staffs = [ staff.serialize() for staff in staffs]
    return render_template("signup.html", staffs=staffs)


@app.route("/signin", methods=["GET", "POST"])
def signin_route():
    return render_template("signin.html")

@app.route("/login", methods=["GET"])
def login_route():
    return redirect(url_for("signin_route"))

# TODO guarded route
@app.route("/users", methods=["GET", "POST"])
def users_route():
    if(request.method == "POST"):
        if(new_user(request.form)):
            return "Success"
        else:
            return "Couldn't add new user!"

    if(request.method == "GET"):
        users = get_users()
        users = []
        users = [ user.serialize() for user in users]
        return render_template("users.html", users=users)

# TODO guarded route
@app.route("/users/<user_id>", methods=["GET", "PUT", "PATCH"])
def user_route(user_id):
    if(request.method == "GET"):
        pass
    if(request.method == "PUT" or request.method == "PATCH"):
        pass

# TODO guarded route
@app.route("/staffs", methods=["GET", "POST"])
def staffs_route():
    if(request.method == "POST"):
        if(new_staff(request.form)):
            return "Success"
        else:
            return "Couldn't add new user!"

    if(request.method == "GET"):
        staffs = get_staffs()
        staffs = [ staff.serialize() for staff in staffs]
        return render_template('staffs.html', staffs=staffs)

# TODO guarded route
@app.route("/departments", methods=["GET", "POST"])
def departments_route():
    if(request.method == "POST"):

        response = new_department(request.form)
        return {"message": response}

    if(request.method == "GET"):

        return render_template("index.html")

# TODO guarded route
@app.route("/keys", methods=["GET", "POST"])
def keys_route():
    if(request.method == "POST"):

        response = new_key(request.form)
        return {"message": response}

    if(request.method == "GET"):

        return render_template("keys.html")

# TODO guarded route
@app.route("/keys/<keyno>", methods=["GET", "PUT", "PATCH"])
def key_route(keyno):
    if(request.method == "PUT" or request.method == "PATCH"):

        response = new_key(request.form)
        return {"message": response}

    if(request.method == "GET"):
        return render_template("keys.html")
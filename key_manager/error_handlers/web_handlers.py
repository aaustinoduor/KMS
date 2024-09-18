from flask import redirect, render_template, url_for


def server_error(code):
    return render_template("500.html")


def method_not_allowed(code):
    return render_template("405.html")


def page_not_found(code):
    return render_template("404.html")


def not_authorised(code):
    return render_template("403.html")


def unauthorised(code):
    return redirect(url_for("index_route.not_authorised"))

from flask import render_template, url_for, redirect, request, Blueprint


auth_route = Blueprint("auth_route", __name__, url_prefix="/api/auth")


@auth_route.post("/signin")
def signin():
    return "Hello from auth signin"
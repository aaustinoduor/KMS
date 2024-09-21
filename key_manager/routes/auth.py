from flask import render_template, url_for, redirect, request, Blueprint, jsonify


auth_route = Blueprint("auth_route", __name__, url_prefix="/api/auth")


@auth_route.get("/signin")
def signin():
    return jsonify(msg="Hello from auth signin")
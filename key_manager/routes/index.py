from flask import render_template, url_for, redirect, request, Blueprint


index_route = Blueprint("index_route", __name__)


@index_route.get("/")
def root():
    return "Hello from root"
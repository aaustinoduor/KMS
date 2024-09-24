from flask import Blueprint


index_route = Blueprint("index_route", __name__, url_prefix="/")


@index_route.get("")
def root():
    """"""
    return "Hello"

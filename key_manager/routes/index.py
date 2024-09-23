import os
from flask import (render_template, url_for, redirect, request, Blueprint,
                   send_from_directory, send_file)


index_route = Blueprint("index_route", __name__, url_prefix="/")


@index_route.get("")
def root():
    """"""
    return render_template('index.html')

from flask import Flask, redirect, render_template, url_for
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.errorhandler(500)
def server_error(code):
    return render_template("500.html")


@app.errorhandler(405)
def method_not_allowed(code):
    return render_template("405.html")


@app.errorhandler(404)
def page_not_found(code):
    return render_template("404.html")


@app.errorhandler(403)
def not_authorised(code):
    return render_template("403.html")


@app.errorhandler(401)
def unauthorised(code):
    return redirect(url_for(not_authorised))

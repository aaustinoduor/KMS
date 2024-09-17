import os
from .app_init import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class Base(DeclarativeBase):
  pass


db = SQLAlchemy(app, model_class=Base)
from flask_vite import Vite
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.orm import declarative_base

base = declarative_base()


fv = Vite()
fc = CORS()
fm = Migrate()
fs = Session()
flask_db = SQLAlchemy(model_class=base)
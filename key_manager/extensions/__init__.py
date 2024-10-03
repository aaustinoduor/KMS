from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import declarative_base

Base = declarative_base()


fc = CORS()
fm = Migrate()
fs = Session()
ma = Marshmallow()
flask_db = SQLAlchemy(model_class=Base)
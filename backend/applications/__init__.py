from flask_bcrypt import Bcrypt
from flask import Flask
from flask_cors import CORS
from applications.models import db, User
from config import Config
from sqlalchemy import event
from sqlalchemy.engine import Engine
import os

bcrypt = Bcrypt()
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

CORS(app, supports_credentials=True)

app.app_context().push()

from applications import routes
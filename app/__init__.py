from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from config import Config
from flask_migrate import Migrate


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
#login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    #login_manager.init_app(app)

    from . import models

    from .auth import auth  
    from .notes import notes
    app.register_blueprint(auth)
    app.register_blueprint(notes)

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from config import Config


db = SQLAlchemy()
jwt = JWTManager()
#login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    #login_manager.init_app(app)


    from .auth import auth  # You’ll create these files soon
    from .notes import notes
    app.register_blueprint(auth)
    app.register_blueprint(notes)

    return app

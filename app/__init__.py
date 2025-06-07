from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()
#login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '09bda9db4c373ac295a272b37f706f9eddab5b3b1c37ca3e985a9da1c7f6bc08'  # Change to something secure
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://saharsmac@localhost/notes_db'
    app.config['JWT_SECRET_KEY'] = 'bcc52b3f85c401ad74d281124a6a82ac1d6ea317ba4afe7724ca57b4f37df802' 

    db.init_app(app)
    jwt.init_app(app)
    #login_manager.init_app(app)


    from .auth import auth  # You’ll create these files soon
    from .notes import notes
    app.register_blueprint(auth)
    app.register_blueprint(notes)

    return app

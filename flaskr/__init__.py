# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
import flask_login

login_manager = flask_login.LoginManager()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysite'
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/sample"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    from flaskr.views import bp
    app.register_blueprint(bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return app
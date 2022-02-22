from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
db.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Model.db"
app.config["SECRET_KEY"] = "l2o1msane2saz"
bcrypts = Bcrypt()
bcrypts.init_app(app)


login_man = LoginManager()
login_man.login_view = "/home"
login_man.init_app(app)
from website import routes

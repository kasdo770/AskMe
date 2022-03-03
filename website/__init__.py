from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, static_folder="static")
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Model.db"
app.config["SECRET_KEY"] = "l2o1msane2saz"
bcrypts = Bcrypt(app)

login_man = LoginManager(app)
login_man.login_view = "/home"
login_man.login_message = "لا يمكنك الذهاب بدون تسجيل الدخول"
from website import routes


from .auth import auth
from .views import views

app.register_blueprint(auth,url_prefix="/")
app.register_blueprint(views,url_prefix="/")


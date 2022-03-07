from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__, static_folder="static")
db = SQLAlchemy(app)
app.config.from_pyfile("config.cfg")
bcrypts = Bcrypt(app)
mail = Mail(app)

login_man = LoginManager(app)
login_man.login_view = "/home"
login_man.login_message = "لا يمكنك الذهاب بدون تسجيل الدخول"
from website import routes


from .auth import auth
from .views import views

app.register_blueprint(auth,url_prefix="/")
app.register_blueprint(views,url_prefix="/")


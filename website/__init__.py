from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__, static_folder="static")
db = SQLAlchemy(app)

mail_settings = {
    'MAIL_SERVER':"smtp.gmail.com",
    'MAIL_USERNAME':'askme9210@gmail.com',
    'MAIL_DEFAULT_SENDER':'askme9210@gmail.com',
    'MAIL_PASSWORD':"",
    'MAIL_PORT':465,
    'MAIL_USE_SSL':True,
    'MAIL_USE_TSL':False,
    'MAIL_DEBUG':True,
    'SECRET_KEY':"l2o1msane2saz",
    'SQLALCHEMY_DATABASE_URI':"sqlite:///Model.db"
}

app.config.update(mail_settings)

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


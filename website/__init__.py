from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Model.db"
app.config["SECRET_KEY"] = "l2o1msane2saz"

from website import routes

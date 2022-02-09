from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""
.box-conatainer{
          margin-top: 145px;
          width: 200px;
          height: 200px;
          border: 10px;
          padding: 5px;
          border-radius: 12px; 
          border-color: green;
        }
"""
app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Model.db"
app.config["SECRET_KEY"] = "l2o1msane2saz"

from website import routes

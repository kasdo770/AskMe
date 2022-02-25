from enum import unique
from flask_login.login_manager import LoginManager
from website import db, login_man
from website import bcrypts
from flask_login import UserMixin
from datetime import date
from sqlalchemy.sql import func

@login_man.user_loader
def load_user(id_user):
    std = Student.query.get(int(id_user)) 
    tea = Teacher.query.get(int(id_user))
    if std:
        return std
    elif tea:
        return tea

class Student(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    custom_id = db.Column(db.String(), unique=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    schooltype = db.Column(db.String(), nullable=False)
    age = db.Column(db.String(), nullable=False)
    posts = db.relationship("ThePost",backref="user",passive_deletes=True)

    @property
    def password(self):
        return self.password    

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypts.generate_password_hash(plain_text_password).decode("utf-8")

    def password_check(self,thepass):
        return bcrypts.check_password_hash(self.password_hash, thepass)

class Teacher(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    custom_id = db.Column(db.String(), unique=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    first_subject = db.Column(db.String(), nullable=False)
    second_subject = db.Column(db.String())

    

    @property
    def password(self):
        return self.password    

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypts.generate_password_hash(plain_text_password).decode("utf-8")

    def password_check(self,thepass):
        return bcrypts.check_password_hash(self.password_hash, thepass)


class ThePost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable = False)
    description = db.Column(db.String() , nullable = False)
    subject = db.Column(db.String(), nullable=False)
    datetime= db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer(), db.ForeignKey("student.id",ondelete="CASCADE"), nullable=False)
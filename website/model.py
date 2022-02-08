from sqlalchemy import Date
from website import db


class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(Length=50), nullable=False)
    password = db.Column(db.String(Length=50), nullable=False)
    SchoolType = db.Column(db.String(), nullable=False)
    Post = db.relationship('Post', backref="owned_user", lazy=True)

class Teacher(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(Length=50), nullable=False)
    password = db.Column(db.String(Length=50), nullable=False)
    First_Subject = db.Column(db.String(), nullable=False)
    Second_Subject = db.Column(db.String())
    Third_Subject = db.Column(db.String())


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String())
    description = db.Column(db.String(Length=8), nullable = False)
    owner = db.Column(db.Integer(), db.ForeignKey('student.id'))

from website import db


class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(Length=50), nullable=False)
    password = db.Column(db.String(Length=50), nullable=False)
    SchoolType = db.Column(db.String(), nullable=False)

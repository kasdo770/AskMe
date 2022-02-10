from flask_login.login_manager import LoginManager
from website import db, login_man
from website import bcrypts
from flask_login import UserMixin

@login_man.user_loader
def load_user(id_user):
    return Student.query.get(int(id_user)) , Teacher.query.get(int(id_user))

class Student(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    schooltype = db.Column(db.String(), nullable=False)
    age = db.Column(db.String(), nullable=False)
    post = db.relationship('Post', backref="owned_user", lazy=True)

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
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    First_Subject = db.Column(db.String(), nullable=False)
    Second_Subject = db.Column(db.String())
    Third_Subject = db.Column(db.String())

    


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String())
    description = db.Column(db.String(), nullable = False)
    owner = db.Column(db.Integer(), db.ForeignKey('student.id'))

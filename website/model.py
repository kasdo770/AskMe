from flask_login.login_manager import LoginManager
from website import db, login_man
from sqlalchemy.sql import expression 
from website import bcrypts
from flask_login import UserMixin
from sqlalchemy.sql import func

@login_man.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    kind = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    schooltype = db.Column(db.String())
    age = db.Column(db.String())
    first_subject = db.Column(db.String())
    second_subject = db.Column(db.String())
    verified = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post",backref="user",passive_deletes=True)
    comments = db.relationship("Comment", backref="user", passive_deletes=True)
    likes = db.relationship("Like", backref="user", passive_deletes=True)

    @property
    def password(self):
        return self.password    

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypts.generate_password_hash(plain_text_password).decode("utf-8")

    def password_check(self,thepass):
        return bcrypts.check_password_hash(self.password_hash, thepass)



class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String())
    datetime= db.Column(db.DateTime(), default=func.now())
    author = db.Column(db.Integer(), db.ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    comments = db.relationship("Comment", backref="posts", cascade="all, delete-orphan")
    likes = db.relationship("Like", backref="posts", cascade="all, delete-orphan")



class Like(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    datetime= db.Column(db.DateTime(), default=func.now())
    author = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    post = db.Column(db.Integer(), db.ForeignKey("post.id", ondelete="CASCADE"))

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String())
    datetime= db.Column(db.DateTime(), default=func.now())
    author = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    post = db.Column(db.Integer(), db.ForeignKey("post.id", ondelete="CASCADE"))

class Problem(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    datetime= db.Column(db.DateTime(), default=func.now())
    author = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
from flask import Blueprint,redirect,url_for,render_template,request,flash
from flask_login import login_required,logout_user,current_user
from website import db
from .model import Post,User,Comment
from website.forms import CommentForm

views = Blueprint("views", __name__)


@views.route("/view-post/<id>")
@login_required
def View_Post(id):
    post = Post.query.filter_by(id=id).first()
    form = CommentForm()
    if not post:
        flash("هذا السؤال غير موجود من قبل", category="error")
        return redirect(url_for("views.MainPage"))
    else:
        return render_template("ViewPost.html",post=post,form=form)

@views.route("/profile")
@login_required
def ProfilePage():
    post = Post.query.all()
    return render_template("profile.html",post=post)



@views.route("/mainpage", methods=["POST","GET"])
@login_required
def MainPage():
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == "POST" and 'filter' in request.form:
        sort_by = request.form.get("filter")
        if sort_by != "none":
            post = Post.query.filter_by(subject=sort_by)
        elif sort_by == "none":
            post = Post.query.all()
        second_post = ""
    elif request.method == "POST" and 'searchinput' in request.form:
        _searchinput = request.form['searchinput']
        post = post.query.filter_by(Post.description.like('%' + _searchinput + '%'))
        post = post.query.order_by(Post.datetime).all()
    else:
        second_post = ""
        post = ""
        if user.first_subject is None:
            post = Post.query.all()
        elif user.first_subject is not None:
            post = Post.query.filter_by(subject=user.first_subject)
            if user.second_subject != "none":
                second_post = Post.query.filter_by(subject=user.second_subject)
    
    
    return render_template("mainpage.html",teacher=user,post=post,second_post=second_post)



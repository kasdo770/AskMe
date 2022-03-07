from website import app,db
from flask_mail import Message
from flask import render_template, url_for, redirect,flash
from website.model import User , Post,Comment
from flask import request
from .views import views
from .auth import auth
from flask_login import login_required,current_user
from website.forms import StudentRegisterForm,TeacherRegisterForm,CommentForm,PostForm,LoginForm,UpdatePostForm


#temporay function
@app.route("/ct")
@app.route("/cleartable")
def cleartable():
    db.drop_all()
    db.create_all()
    return render_template("homepage.html")


#----------
@app.route("/home")
@app.route("/")
def HomePage():
    posts = Post.query.all()
    number_of_posts = 0
    number_of_post = ""
    for post in posts:
        number_of_posts +=1
    if len(str(number_of_posts)) >=4 :
        number_of_post = f"{str(number_of_posts)[:-3]},{str(number_of_posts)[-3:]}"
    elif int(number_of_posts) == 0:
        number_of_post = "لا توجد اي اسئلة"
    else:
        number_of_post = number_of_posts
    return render_template("homepage.html",number_of_posts=number_of_post)



@app.route("/create/post", methods=["POST", "GET"])
@login_required
def CreatePostPage():
    if current_user.kind == "student":
        form = PostForm()
        if form.validate_on_submit():
            if form.create.data:
                new_post = Post(
                    title=form.title.data,
                    description=form.description.data,
                    subject = form.subject.data,
                    update_description = "",
                    author = current_user.id
                )
                db.session.add(new_post)
                db.session.commit()
                flash("لقد تم انشاء سؤال بنجاح", category="success")
                return redirect(url_for("views.MainPage"))

            elif form.cancel.data:
                return redirect(url_for("views.MainPage"))
    elif current_user.kind == "teacher":
        flash("لا يمكنك انشاء سؤال ب حساب معلم",category="error")
        return redirect(url_for("views.MainPage"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )

    return render_template("CreatePost.html", form=form)




@app.route("/delete-post/<id>")
@login_required
def Delete_Post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:

        flash("هذا السؤال غير موجود من قبل", category="error")

    elif current_user.id != post.user.id:
        flash("انت لست صاحب السؤال . لا تملك صلاحية لحذفه", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("لقد تم مسح السؤال بنجاح" , category="success")

    return redirect(url_for("views.MainPage"))




@app.route("/update-post/<id>", methods=["POST", "GET"])
@login_required
def Update_Post(id):
    filled = False
    post = Post.query.filter_by(id=id).first()
    form = UpdatePostForm()
    if not post:
        flash("هذا السؤال غير موجود من قبل", category="error")
        return redirect(url_for("views.MainPage"))
    else:
        if form.validate_on_submit():
            if form.cal.data:
                return redirect(url_for("views.MainPage"))
            if form.crt.data:
                post.update_description = ""
                db.session.commit()
                updated_post = Post(
                    id = post.id,
                    title= post.title,
                    description= post.description,
                    update_description = form.description.data,
                    subject = form.subject.data,
                    author = current_user.id
                )
                db.session.delete(post)
                db.session.merge(updated_post)
                db.session.commit()
                flash("لقد تم تحديث سؤال بنجاح", category="success")
                return redirect(url_for("views.MainPage"))

    return render_template("UpdatePost.html", form=form , filled=filled)

        
@app.route("/create/comment/<post_id>", methods=["POST","GET"])
def CreateComment(post_id):
    form = CommentForm()
    post = Post.query.filter_by(id=post_id)
    if post:
        if form.validate_on_submit():
            if form.cancel.data:
                return redirect(url_for(f"views.View_Post",id=post_id))
            elif form.create.data:
                new_comment = Comment(
                    description = form.description.data,
                    author = current_user.id,
                    post = post_id
                )
                db.session.add(new_comment)
                db.session.commit()
    else:
        print("no")
    return render_template("CreateComment.html", form=form)

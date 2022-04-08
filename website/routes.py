from website import app,db,mail
from flask_mail import Message
from flask import render_template, url_for, redirect,flash
from website.model import Like, User , Post,Comment,Problem
from flask import request
from .views import views
from .auth import auth
from flask_login import login_required,current_user
from website.forms import StudentRegisterForm,TeacherRegisterForm,PostForm,LoginForm,UpdatePostForm,SupportForm,AdminForm


#temporay function
@app.route("/ct")
@app.route("/cleartable")
def cleartable():
    db.drop_all()
    db.create_all()
    return redirect(url_for('HomePage'))

@app.route('/admin/add',methods=["POST",'GET'])
@login_required
def Admin_Add():
    form = AdminForm()
    if current_user.kind == 'admin' or current_user.id == 1:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            user.kind = 'admin'
            flash('لقد تم التغيير بنجاح',category="success")
            db.session.commit()
            return redirect(url_for('views.MainPage'))
    else:
        return redirect(url_for('views.MainPage'))
        

    if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f"هنالك مشكلة في :  {err_msg}", category="error"
                )
    return render_template('admin.html',form = form)


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


@app.route('/delete-comment/<comment_id>/<post_id>')
def DeleteComment(comment_id,post_id):
    post = Post.query.filter_by(id=post_id).first()
    comment = Comment.query.filter_by(id=comment_id).first()
    if not post:
        flash("هذا السؤال غير موجود")
    elif not comment:
        flash('هذه الاجابة غير موجودة ')
    elif current_user.kind == 'admin':
        db.session.delete(comment)
        db.session.commit()
    elif current_user.id != comment.user.id:
        flash('انت لست صاحب الاجابة, لا تملك صلاحية لحذفها')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.View_Post',id=post.id))
        


@app.route("/create/post", methods=["POST", "GET"])
@login_required
def CreatePostPage():
    form = PostForm()
    if current_user.verified == 1:
        if current_user.kind == "student" or current_user.kind=="admin":
            if form.validate_on_submit():
                if form.create.data:
                    new_post = Post(
                        title=form.title.data,
                        description=form.description.data,
                        subject = form.subject.data,
                        author = current_user.id,
                    )
                    db.session.add(new_post)
                    db.session.commit()
                    flash("لقد تم انشاء سؤال بنجاح", category="success")
                    return redirect(url_for("views.MainPage"))

                elif form.cancel.data:
                    return redirect(url_for("views.MainPage"))
        elif current_user.kind == "teacher":
            flash("لا يمكنك انشاء سؤال بحساب معلم",category="error")
            return redirect(url_for("views.MainPage"))

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f"هنالك مشكلة في :  {err_msg}", category="error"
                )
    else:
        flash('لا يمكنك انشاء سؤال بدون تفعيل حسابك')
        return redirect(url_for('views.MainPage'))
    return render_template("create-post.html", form=form)




@app.route("/delete-post/<id>")
@login_required
def Delete_Post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:

        flash("هذا السؤال غير موجود", category="error")
    elif current_user.kind == 'admin':
        db.session.delete(post)
        db.session.commit()
    elif current_user.id != post.user.id:
        flash("انت لست صاحب السؤال , لا تملك صلاحية لحذفه", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("لقد تم مسح السؤال بنجاح" , category="success")

    return redirect(url_for("views.MainPage"))




@app.route("/update-post/<id>", methods=["POST", "GET"])
@login_required
def Update_Post(id):
    form = UpdatePostForm()
    post = Post.query.filter_by(id=id).first()
    if current_user.id != post.user.id:
        flash("انت لا تملك الصلاحية لتعديل السؤال , فقط السائِل يملك هذه الصلاحية", category="error")
        return redirect(url_for('views.MainPage'))
    else:
        if not post:
            flash("هذا السؤال غير موجود", category="error")
            return redirect(url_for("views.MainPage"))
        else:
                if form.validate_on_submit():
                    if form.cal.data:
                        return redirect(url_for("views.MainPage"))
                    if form.crt.data:
                        post.description = request.form.get('desc')
                        db.session.commit()
                        flash("لقد تم تحديث السؤال بنجاح", category="success")
                        return redirect(url_for("views.MainPage"))
        return render_template("UpdatePost.html", form=form,post=post)



@app.route('/support',methods=['POST','GET'])
def Support():
    form = SupportForm()
    if form.validate_on_submit():
        if form.create.data:
            new_problem = Problem(
                description = form.description.data,
                title = form.title.data,
                subject = form.subjects.data,
                author = current_user.id,
            )
            db.session.add(new_problem)
            db.session.commit()
            msg = Message('الدعم' , sender=current_user.email , recipients=["askme9210@gmail.com"])
            msg.html = render_template('supportmail.html',user=current_user.username,desc=form.description.data, sub = form.subjects.data,title = form.title.data)
            mail.send(msg)
            return redirect(url_for('views.MainPage'))
        else:
            return redirect(url_for('views.MainPage'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )
    return render_template('Support.html',form=form)
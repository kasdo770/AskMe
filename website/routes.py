from flask_login import current_user, login_required
from website import app,db
from flask import render_template, url_for, redirect,flash
from website.forms import StudentRegisterForm, LoginForm,TeacherRegisterForm, PostForm
from website.model import Post, Student , Teacher
#from datetime import datetime as dt
import time

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
    return render_template("homepage.html")

@app.route("/create/post", methods=["POST", "GET"])
def CreatePostPage():
    form = PostForm()
    if form.validate_on_submit():
        if form.create.data:
            new_post = Post(
                title=form.title.data,
                description = form.description.data,
                subject = form.subject.data,
                date = time.ctime()

            )
            db.session.add(new_post)
            db.session.commit()
            flash("لقد تم انشاء سؤال بنجاح",category="success")
            return render_template("homepage.html")
        elif form.cancel.data:
            return render_template("")

    return render_template("CreatePost.html", form=form)

@app.route("/register/std", methods = ["POST", "GET"])
def StudentRegisterPage():
    form = StudentRegisterForm()
    if form.validate_on_submit():
        new_student = Student(
           username=form.username.data,
           password = form.password1.data,
           email=form.email.data,
           schooltype=form.schooltype.data,
           age = form.age.data
        )
        flash(f"تم انشاء حساب طالب جديد باسم{form.username.data}" , category="success")
        db.session.add(new_student)
        db.session.commit()
        return render_template("homepage.html")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"The was an an Error with creating user :  {err_msg}", category="error"
            )

    return render_template("Student_register.html", form=form)


@app.route("/register/tea", methods = ["POST", "GET"])
def TeacherRegisterPage():
    form = TeacherRegisterForm()
    print("first")
    if form.validate_on_submit():
        print("second")
        new_teacher = Teacher(
           username=form.username.data,
           password = form.password1.data,
           email=form.email.data,
           first_subject=form.first_subject.data,
           second_subject = form.second_subject.data
        )
        flash(f"تم انشاء حساب معلم جديد باسم {form.username.data}", category="success")
        db.session.add(new_teacher)
        db.session.commit()
        return redirect(url_for("HomePage"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"The was an an Error with creating user :  {err_msg}", category="error"
            )
    return render_template("Teacher_register.html", form=form)


@app.route("/login" ,methods = ["POST", "GET"])
def LoginPage():
    form = LoginForm()
    if form.validate_on_submit():
        student_user = Student.query.filter_by(username=form.username.data).first()
        teacher_user = Teacher.query.filter_by(username=form.username.data).first()
        print("Stop")
        if student_user:
            print("student")
            if student_user.password_check(thepass=form.password.data):
                flash(
                    f"تم تسجيل الدخول بنجاح يا  {form.username.data}",
                    category="success",
                ) 
                print("تم تسجيل الدخول ب نجاح")
                return redirect(url_for("HomePage"))
            else:
                flash("كلمة المرور خاطئا", category="error")
                
        elif teacher_user:
            print("student")
            if teacher_user.password_check(thepass=form.password.data):
                flash(
                    f"تم تسجيل الدخول بنجاح يا  {form.username.data}",
                    category="success",
                )
                print("Logged in successfuly")
                return redirect(url_for("HomePage"))
            else:
                flash("كلمة المرور خاطئا", category="error")
                
        else:
            flash("ليس هنالك اي حساب بهذ الاسم", category="error")

    return render_template("Login.html", form=form)


@login_required
@app.route("/mainpage", methods=["GET"])
def MainPage():
    post = Post.query.all()
    return render_template("mainpage.html" ,post=post)
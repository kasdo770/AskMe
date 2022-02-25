from flask_login import current_user, login_required, login_user, logout_user
from website import app,db,login_man
from flask import render_template, url_for, redirect,flash
from website.forms import StudentRegisterForm, LoginForm,TeacherRegisterForm, PostForm
from website.model import Student , Teacher, ThePost
import secrets



#temporay function
@app.route("/ct")
@app.route("/cleartable")
def cleartable():
    db.drop_all()
    db.create_all()
    return render_template("homepage.html")


@app.route("/logout")
@login_required
def Logout():
    logout_user()
    return redirect(url_for("HomePage"))
#----------
@app.route("/home")
@app.route("/")
def HomePage():
    return render_template("homepage.html")

@app.route("/create/post", methods=["POST", "GET"])
@login_required
def CreatePostPage():
    form = PostForm()
    if form.validate_on_submit():
        if form.create.data:
            new_post = ThePost(
                title=form.title.data,
                description=form.description.data,
                subject = form.subject.data,
                author = current_user.id
            )
            db.session.add(new_post)
            db.session.commit()
            flash("لقد تم انشاء سؤال بنجاح", category="success")
            return redirect(url_for("MainPage"))
        elif form.cancel.data:
            return redirect(url_for("MainPage"))
    return render_template("CreatePost.html", form=form)

@app.route("/register/std", methods = ["POST", "GET"])
def StudentRegisterPage():
    form = StudentRegisterForm()
    phrase1 = secrets.token_hex(16)  
    final_answer = str(phrase1)
    if form.validate_on_submit():   
        new_student = Student(
           custom_id = final_answer,
           username=form.username.data,
           password = form.password1.data,
           email=form.email.data,
           schooltype=form.schooltype.data,
           age = form.age.data
        )
        flash(f" تم انشاء حساب طالب جديد باسم{form.username.data}" , category="success")
        db.session.add(new_student)
        db.session.commit()
        login_user(new_student, remember=True)
        current_user.custom_id = final_answer
        return render_template("homepage.html")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )

    return render_template("Student_register.html", form=form)


@app.route("/register/tea", methods = ["POST", "GET"])
def TeacherRegisterPage():
    form = TeacherRegisterForm()
    phrase1 = secrets.token_hex(16)  
    final_answer = str(phrase1)
    if form.validate_on_submit():
        new_teacher = Teacher(
           custom_id = final_answer,
           username=form.username.data,
           password = form.password1.data,
           email=form.email.data,
           first_subject=form.first_subject.data,
           second_subject = form.second_subject.data
        )
        flash(f" تم انشاء حساب معلم جديد باسم {form.username.data}", category="success")
        db.session.add(new_teacher)
        db.session.commit()
        login_user(new_teacher, remember=True)
        current_user.custom_id = final_answer
        return redirect(url_for("HomePage"))
    if form.errors != {}:
        for err_msg in form.errors.values():
             flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )
    return render_template("Teacher_register.html", form=form)



@app.route("/login" ,methods = ["POST", "GET"])
def LoginPage():
    form = LoginForm()
    if form.validate_on_submit():
        student_user = Student.query.filter_by(username=form.username.data).first()
        teacher_user = Teacher.query.filter_by(username=form.username.data).first()
        if student_user:
            if student_user.password_check(thepass=form.password.data):
                flash(
                    f"تم تسجيل الدخول بنجاح يا  {form.username.data}",
                    category="success",
                ) 
                login_user(student_user, remember=True)
                print(current_user.custom_id)
                return redirect(url_for("HomePage"))
            else:
                flash("كلمة المرور خاطئا", category="error")
                
        elif teacher_user:
            if teacher_user.password_check(thepass=form.password.data):
                flash(
                    f"تم تسجيل الدخول بنجاح يا  {form.username.data}",
                    category="success",
                )

                login_user(teacher_user, remember=True)
                print(current_user.custom_id)
                print("Logged in successfuly")
                return redirect(url_for("HomePage"))
            else:
                flash("كلمة المرور خاطئا", category="error")
                
        else:
            flash("ليس هنالك اي حساب بهذ الاسم", category="error")

    return render_template("Login.html", form=form)


@app.route("/mainpage", methods=["GET"])
@login_required
def MainPage():
    post = ThePost.query.all()
    print(current_user.custom_id)
    return render_template("mainpage.html",post=post,user=current_user)


@app.route("/profile")
def ProfilePage():
    print(current_user.custom_id)
    return render_template("profile.html", user=current_user)
from flask_login import current_user
from website import app,db
from flask import render_template, url_for, redirect,flash
from website.forms import StudentRegisterForm, LoginForm,TeacherRegisterForm
from website.model import Student , Teacher

#temporay function
@app.route("/ct")
@app.route("/cleartable")
def cleartable():
    db.drop_all()
    db.create_all()
    return render_template("base.html")

#----------
@app.route("/home")
@app.route("/")
def HomePage():
    return render_template("base.html")


@app.route("/register/std", methods = ["POST", "GET"])
def StudentRegisterPage():
    form = StudentRegisterForm()
    db.create_all()
    if form.validate_on_submit():
        new_student = Student(
           username=form.username.data,
           password = form.password1.data,
           email=form.email.data,
           schooltype=form.schooltype.data,
           age = form.age.data
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for("HomePage"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"The was an an Error with creating user :  {err_msg}", category="error"
            )

    return render_template("Student_register.html", form=form)


@app.route("/register/tea", methods = ["POST", "GET"])
def TeacherRegisterPage():
    form = TeacherRegisterForm()
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
                    f"تم تسجيل الدخول بنجاح ايها الطالب {form.username.data} ",
                    category="success",
                ) 
                print("Logged in successfuly")
                return redirect(url_for("HomePage"))
            else:
                flash("كلمة المرور خاطئا", category="error")
                
        elif teacher_user:
            print("student")
            if teacher_user.password_check(thepass=form.password.data):
                flash(
                    f"تم تسجيل الدخول بنجاح ايها المعلم  {form.username.data}",
                    category="success",
                )
                print("Logged in successfuly")
                return redirect(url_for("HomePage"))
            else:
                flash("كلمة المرور خاطئا", category="error")
                
        else:
            flash("ليس هنالك اي حساب بهذ الاسم", category="error")

    return render_template("Login.html", form=form)

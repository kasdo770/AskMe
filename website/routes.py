from website import app
from flask import render_template, url_for
from website.forms import StudentRegisterForm, StudentLoginForm, TeacherLoginForm,TeacherRegisterForm


@app.route("/home")
@app.route("/")
def HomePage():
    return render_template("base.html")


@app.route("/register/std")
def StudentRegisterPage():
    form = StudentRegisterForm()
    return render_template("Student_register.html", form=form)


@app.route("/login/std")
def StudentLoginPage():
    form = StudentLoginForm()
    return render_template("Student_login.html", form=form)

@app.route("/register/tea")
def TeacherRegisterPage():
    form = TeacherRegisterForm()
    return render_template("Teacher_register.html", form=form)


@app.route("/login/tea")
def TeacherLoginPage():
    form = TeacherLoginForm()
    return render_template("Teacher_login.html", form=form)

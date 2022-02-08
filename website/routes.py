from website import app
from flask import render_template, url_for
from website.forms import StudentRegisterForm, LoginForm,TeacherRegisterForm


@app.route("/home")
@app.route("/")
def HomePage():
    return render_template("base.html")


@app.route("/register/std")
def StudentRegisterPage():
    form = StudentRegisterForm()
    return render_template("Student_register.html", form=form)


@app.route("/register/tea")
def TeacherRegisterPage():
    form = TeacherRegisterForm()
    return render_template("Teacher_register.html", form=form)


@app.route("/login")
def LoginPage():
    form = LoginForm()
    return render_template("Teacher_login.html", form=form)

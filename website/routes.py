from website import app
from flask import render_template, url_for
from website.forms import StudentRegisterForm


@app.route("/home")
@app.route("/")
def HomePage():
    return render_template("base.html")


@app.route("/register")
def RegisterPage():
    form = StudentRegisterForm()
    return render_template("register.html", form=form)


@app.route("/login")
def LoginPage():
    return render_template("login.html")

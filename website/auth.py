from flask import Blueprint,redirect,url_for,flash,render_template
from flask_login import login_required,logout_user,current_user,login_user
from website import db
from .model import User,Post,Comment
from website.forms import StudentRegisterForm, LoginForm,TeacherRegisterForm, PostForm, UpdatePostForm,CommentForm


auth = Blueprint("auth", __name__)


@auth.route("/login" ,methods = ["POST", "GET"])
def LoginPage():
    print(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        if current_user:
            logout_user()
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.kind =="student":
                if user.password_check(thepass=form.password.data):
                    flash(
                        f" تم تسجيل الدخول بنجاح يا ايها  طالب {form.username.data}",
                        category="success",
                    ) 
                    login_user(user, remember=True)
                    print(current_user)
                    return redirect(url_for("HomePage"))
                else:
                    flash("كلمة المرور خاطئا", category="error")
                    
            if user.kind == "teacher":
                if user.password_check(thepass=form.password.data):
                    flash(
                        f"تم تسجيل الدخول بنجاح يا ايها مستر {form.username.data}",
                        category="success",
                    )
                    login_user(user, remember=True)
                    print(current_user)
                    print("Logged in successfuly")
                    return redirect(url_for("HomePage"))
                else:
                    flash("كلمة المرور خاطئا", category="error")
                    
            else:
                flash("ليس هنالك اي حساب بهذ الاسم", category="error")
        else:
            flash("لا يوجد يا مستخدم بهذا الاسم",category="error")

    return render_template("Login.html", form=form)



@auth.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for("HomePage"))



@auth.route("/register/tea", methods = ["POST", "GET"])
def TeacherRegisterPage():
    print(current_user)
    form = TeacherRegisterForm()

    if form.validate_on_submit():
        if current_user:
            logout_user()
        new_teacher = User(
           username=form.username.data,
           password = form.password1.data,
           email=form.email.data,
           kind="teacher",
           first_subject=form.first_subject.data,
           second_subject = form.second_subject.data
        )
        flash(f" تم انشاء حساب معلم جديد باسم {form.username.data}", category="success")
        db.session.add(new_teacher)
        db.session.commit()
        login_user(new_teacher, remember=True)
        return redirect(url_for("HomePage"))
    if form.errors != {}:
        for err_msg in form.errors.values():
             flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )
    return render_template("register_tea.html", form=form)


@auth.route("/register/std", methods = ["POST", "GET"])
def StudentRegisterPage():
    form = StudentRegisterForm()  
    if form.validate_on_submit():   
        if current_user:
            logout_user()
        new_student = User(
           username=form.username.data,
           password = form.password1.data,
           email=form.email.data,
           kind = "student",
           schooltype=form.schooltype.data,
           age = form.age.data
        )
        flash(f" تم انشاء حساب طالب جديد باسم{form.username.data}" , category="success")
        db.session.add(new_student)
        db.session.commit()
        login_user(new_student, remember=True)
        return redirect(url_for("HomePage"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )

    return render_template("register_std.html", form=form)

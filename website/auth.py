from flask import Blueprint,redirect,url_for,flash,render_template
from flask_login import login_required,logout_user,current_user,login_user
from website import db,mail
from flask_mail import Message
from .model import User,Post,Comment
from website.forms import StudentRegisterForm, LoginForm,TeacherRegisterForm, PostForm, UpdatePostForm,CommentForm
import secrets as sr


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
    form = TeacherRegisterForm()
    verfication_key = sr.token_hex(4)
    if form.validate_on_submit():
        msg = Message("تاكيد حساب العلم", recipients=[form.email.data])
        msg.body = "يرجي تاكيد حساب المعلم ب هذا الكود عند صفحة التسجيل"
        mail.send(msg)
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
    verfication_key = sr.token_hex(4)
    msg = Message("تاكيد حساب الطالب", recipients=["drtr4p23@gmail.com"])
    msg.html = f"""<h1>السلام عليكم يا {form.username.data}</h1>
        <h3>اهلا بك في موقع اسئلة . للبدء يرجي ادخال الكود الذي امامك 
        في صفحة تسجيل دخول طالب لانشاء حسابك
                    {verfication_key}</h3>
        """
    mail.send(msg)
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

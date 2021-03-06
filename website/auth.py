from functools import reduce
from flask import Blueprint,redirect, request,url_for,flash,render_template
from flask_login import login_required,logout_user,current_user,login_user
from website import db,mail,urlsafe
from itsdangerous import SignatureExpired
from flask_mail import Message
from .model import User,Post,Comment
from website.forms import StudentRegisterForm, LoginForm,TeacherRegisterForm, PostForm, UpdatePostForm


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
                if user.password_check(thepass=form.password.data):
                    flash(
                        f" تم تسجيل الدخول بنجاح يا {form.username.data}",
                        category="success",
                    ) 
                    login_user(user, remember=True)
                    print(current_user)
                    return redirect(url_for("HomePage"))
                else:
                    flash("كلمة المرور خاطئة", category="error")
                    
        else:
            flash("لا يوجد أي مستخدم بهذا الاسم",category="error")

    return render_template("Login.html", form=form)



@auth.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for("HomePage"))


@auth.route("/confirm-email/<token>")
def ConfirmEmail(token):
    email = urlsafe.loads(token,salt='email-confirm')
    user = User.query.filter_by(email=email).first()
    if user:
            try:
                validationemail = urlsafe.loads(token,salt='email-confirm',max_age=300)
                user.verified = True
                db.session.commit()
                login_user(user)
                return redirect(url_for("auth.VerifyEmail",id=current_user.id))
            except SignatureExpired:
                login_user(user)
                return redirect(url_for('auth.VerifyEmail',id=current_user.id))
    else:
        flash('لا يوجد اي مستخدم بهذا الاسم')
    return redirect(url_for('views.MainPage'))
    

@auth.route("/verify-mail/<id>")
def VerifyEmail(id):
    user = User.query.filter_by(id=id).first()
    print(user.email)
    if user.verified == 0:
        token = urlsafe.dumps(current_user.email ,salt='email-confirm')
        msg = Message("تاكيد حسابك", recipients=[current_user.email])
        link = url_for("auth.ConfirmEmail" ,token=token,_external=True)
        msg.html = render_template("Email.html",link=link,user=user)
        mail.send(msg)
    return render_template("verify.html")


@auth.route("/register/tea", methods = ["POST", "GET"])
def TeacherRegisterPage():
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
        login_user(new_teacher)
        return redirect(url_for('views.MainPage'))
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
        flash(f" تم انشاء حساب طالب جديد باسم {form.username.data} " , category="success")
        db.session.add(new_student)
        db.session.commit()
        login_user(new_student)
        return redirect(url_for('views.MainPage'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )

    return render_template("register_std.html", form=form)

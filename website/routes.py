from asyncio.windows_events import NULL
from flask_login import current_user, login_required, login_user, logout_user
from website import app,db
from flask import render_template, url_for, redirect,flash
from website.forms import StudentRegisterForm, LoginForm,TeacherRegisterForm, PostForm, UpdatePostForm
from website.model import User , ThePost

eng_subject = {
        "احياء":"biology",
        "كيمياء":"chemistry",
        "عربي":"arabic",
        "انجليزي":"english",
        "فرنسي":"french",
        "ايطالي":"italy",
        "فلسف":"physiologist",
        "تاريخ":"history",
        "جفراقيا":"geography",
        "رياض":"math",
    }

def Search_Bar(text):
    subjects = ['فيزياء ', 'كيمياء', 'احياء',
    "عربي", "انجليزي", "فرنسي", "ايطالي",
    "فلسف", "جفراقيا", "تاريخ", "رياض"]

    for item in subjects:
        if item in text:
            post = ThePost.query.filter_by(eng_subject.get(item))

        else:
            post = ""

        result = result + " " + post 
    return result   

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



@app.route("/register/std", methods = ["POST", "GET"])
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
        return render_template("homepage.html")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )

    return render_template("Student_register.html", form=form)


@app.route("/register/tea", methods = ["POST", "GET"])
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
    return render_template("Teacher_register.html", form=form)



@app.route("/login" ,methods = ["POST", "GET"])
def LoginPage():
    print(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        if current_user:
            logout_user()
        user = User.query.filter_by(username=form.username.data).first()
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

    return render_template("Login.html", form=form)

@app.route("/profile")
def ProfilePage():
    return render_template("profile.html", user=current_user)



@app.route("/mainpage", methods=["POST","GET"])
@login_required
def MainPage():
    user = User.query.filter_by(id=current_user.id).first()
    second_post = ""
    post = ""
    if user.first_subject is None:
        post = ThePost.query.all()
    elif user.first_subject is not None:
        post = ThePost.query.filter_by(subject=user.first_subject)
        if user.second_subject != "none":
            second_post = ThePost.query.filter_by(subject=user.second_subject)
    return render_template("mainpage.html",teacher=user,post=post,second_post=second_post)

@app.route("/create/post", methods=["POST", "GET"])
@login_required
def CreatePostPage():
    if current_user.kind == "student":
        form = PostForm()
        if form.validate_on_submit():
            if form.create.data:
                new_post = ThePost(
                    title=form.title.data,
                    description=form.description.data,
                    subject = form.subject.data,
                    update_description = "",
                    author = current_user.id
                )
                db.session.add(new_post)
                db.session.commit()
                flash("لقد تم انشاء سؤال بنجاح", category="success")
                return redirect(url_for("MainPage"))

            elif form.cancel.data:
                return redirect(url_for("MainPage"))
    elif current_user.kind == "teacher":
        flash("لا يمكنك انشاء سؤال ب حساب معلم",category="error")
        return redirect(url_for("MainPage"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"هنالك مشكلة في :  {err_msg}", category="error"
            )

    return render_template("CreatePost.html", form=form)




@app.route("/delete-post/<id>")
def Delete_Post(id):
    post = ThePost.query.filter_by(id=id).first()
    if not post:

        flash("هذا السؤال غير موجود من قبل", category="error")

    elif current_user.id != post.user.id:
        flash("انت لست صاحب السؤال . لا تملك صلاحية لحذفه", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("لقد تم مسح السؤال بنجاح" , category="success")

    return redirect(url_for("MainPage"))




@app.route("/view-post/<id>")
def View_Post(id):
    post = ThePost.query.filter_by(id=id).first()
    if not post:
        flash("هذا السؤال غير موجود من قبل", category="error")
        return redirect(url_for("MainPage"))
    else:
        return render_template("ViewPost.html", post=post)




@app.route("/update-post/<id>", methods=["POST", "GET"])
def Update_Post(id):
    filled = False
    post = ThePost.query.filter_by(id=id).first()
    form = UpdatePostForm()
    if not post:
        flash("هذا السؤال غير موجود من قبل", category="error")
        return redirect(url_for("MainPage"))
    else:
        if form.validate_on_submit():
            if form.cal.data:
                return redirect(url_for("MainPage"))
            if form.crt.data:
                post.update_description = ""
                db.session.commit()
                updated_post = ThePost(
                    id = post.id,
                    title= post.title,
                    description= post.description,
                    update_description = form.description.data,
                    subject = form.subject.data,
                    author = current_user.id
                )
                db.session.delete(post)
                db.session.merge(updated_post)
                db.session.commit()
                flash("لقد تم تحديث سؤال بنجاح", category="success")
                return redirect(url_for("MainPage"))

    return render_template("UpdatePost.html", form=form , filled=filled)

        

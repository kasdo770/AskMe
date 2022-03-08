from flask import Blueprint,redirect,url_for,render_template,request,flash
from flask_login import login_required,logout_user,current_user
from website import db
from .model import Post,User,Comment
from website.forms import CommentForm

views = Blueprint("views", __name__)


@views.route("/view-post/<id>",methods=['POST','GET'])
@login_required
def View_Post(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(post=post.id).all()
    form = CommentForm()
    if not post:
        flash("هذا السؤال غير موجود من قبل", category="error")
        return redirect(url_for("views.MainPage"))
    else:
        if form.create.data:
            new_comment = Comment(
                description = form.description.data,
                author = current_user.id,
                post = id
            )
            db.session.add(new_comment)
            db.session.commit()
        return render_template("ViewPost.html",post=post,form=form,comment=comments)

@views.route("/profile", methods=["POST","GET"])
@login_required
def ProfilePage():
    post = Post.query.all()
    if request.method == "POST":
        verifyemail = request.form.get('email')
        verifyusername = request.form.get('username')
        email = User.query.filter_by(email=verifyemail).first()
        username = User.query.filter_by(username=verifyusername).first()
        if username or email:
            flash(" لا يمكنك تعديل من الاسم او الايميل الخاص بك لهذا الاسم او الايميل",category="error")
        else:
            try: 
                current_user.email = request.form.get('email')
                current_user.username = request.form.get('username')
                if current_user.kind == "student":
                    current_user.schooltype = request.form.get('schooltype')
                    current_user.age = request.form.get('age')
                    print(current_user.age)
                    print(current_user.schooltype)
                elif current_user.kind == "teacher":
                    current_user.first_subject = request.form.get('first_subject')
                    current_user.second_subject = request.form.get('second_subject')
                flash("لقد تم التعديل بنجاح",category="info")
            except:
                flash("لا يمكنك تعديل لهذا الاسم او الايميل",category="error")

            db.session.commit()

    return render_template("profile.html",post=post)



@views.route("/mainpage", methods=["POST","GET"])
@login_required
def MainPage():
    user = User.query.filter_by(id=current_user.id).first()
    post = Post.query
    second_post = ""
    if request.method == "POST" and 'filter' in request.form:
        sort_by = request.form.get("filter")
        if sort_by != "none":
            post = Post.query.filter_by(subject=sort_by)
        elif sort_by == "none":
            post = Post.query.all()
        second_post = ""
    elif request.method == "POST" and 'searchinput' in request.form:
        print('search')
        _searchinput = request.form['searchinput']

        post = post.filter(Post.description.like('%' + _searchinput + '%'))
        post = post.order_by(Post.datetime).all()

    else:
        second_post = ""
        post = ""
        if user.first_subject is None:
            post = Post.query.all()
        elif user.first_subject is not None:
            post = Post.query.filter_by(subject=user.first_subject)
            if user.second_subject != "none":
                second_post = Post.query.filter_by(subject=user.second_subject)
    
    
    return render_template("mainpage.html",teacher=user,post=post,second_post=second_post)



from ast import Lambda
import profile
from flask import Blueprint,redirect,url_for,render_template,request,flash,jsonify
from flask_login import login_required,logout_user,current_user
from website import db,urlsafe
from .model import Post,User,Comment,Like

views = Blueprint("views", __name__)


BASE = "https://rocky-escarpment-76791.herokuapp.com"

@views.route('/like-post/<post_id>',methods=["POST","GET"])
@login_required
def Likes(post_id):
    post = Post.query.filter_by(id = post_id).first()
    like = Like.query.filter_by(author=current_user.id,post = post_id).first()
    if current_user.verified == 1:
        if not post:
            return jsonify({'error':'السؤال غير موجود'}, 400)
        elif like:
            db.session.delete(like)
            db.session.commit()
        else:
            new_like = Like(author = current_user.id , post = post_id)

            db.session.add(new_like)
            db.session.commit() 
        
    return jsonify({"likes":len(post.likes) , "liked" : current_user.id in map(lambda x: x.author , post.likes)})



@views.route(f"{BASE}/view-post/<id>",methods=['POST','GET'])
@login_required
def View_Post(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(post=post.id).all()
    user_comments = Comment.query.filter_by(author=current_user.id).count()
    teacher_ordered_comments = []
    for comment in comments:
        if comment.user.kind == "teacher":
            teacher_ordered_comments.append(comment)
    if not post:
        flash("هذا السؤال غير موجود", category="error")
        return redirect(url_for("views.MainPage"))
    else:
        if request.method == "POST":
            if current_user.verified == 1:
                if user_comments <= 2:
                    description = request.form.get('desc')
                    if len(str(description)) != 0:
                        new_comment = Comment(
                            description=description,
                            author=current_user.id,
                            post=post.id
                        )
                        db.session.add(new_comment)
                        db.session.commit()
                        return redirect(url_for("views.View_Post",id=post.id))
                    else:
                        flash("لا يمكنك انشاء اجابة فارغة", category="error")
                else:
                    flash("لا يمكنك انشاء اكثر من 3 اسئلة", category="error")
            else:
                flash("لا يمكنك الاجابة علي السؤال بدون تفعيل حسابك",category="error" )

    return render_template("ViewPost.html",post=post,comment=comments,teacher_comments = teacher_ordered_comments)

@views.route("/profile", methods=["POST","GET"])
@login_required
def ProfilePage():
    post = Post.query.all()
    if request.method == "POST" and 'submitbtn' in request.form:
        verifyusername = request.form.get('username')
        user = User.query.filter_by(username=verifyusername).first()


        if user and user.username != current_user.username:
            flash(" لا يمكنك  تغيير اسم حسابك الي هذا الاسم ",category="error")
        if user and user.email != current_user.email:
            flash(" لا يمكنك  تغيير ايميلك الي هذا الايميل ",category="error")
        else:
            try: 
                current_user.email = request.form.get('email')
                current_user.username = request.form.get('username')
                if current_user.kind == "student":
                    current_user.schooltype = request.form.get('schooltype')
                    current_user.age = request.form.get('age')
                elif current_user.kind == "teacher":
                    current_user.first_subject = request.form.get('first_subject')
                    current_user.second_subject = request.form.get('second_subject')  

                current_user.verified = False
                flash("لقد تم التعديل بنجاح", category="info")
            except:
                flash("لا يمكنك التغيير الي هذا الاسم او الايميل",category="error")

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
            ordered = False
            post = Post.query.filter_by(subject=sort_by)
        elif sort_by == "none":
            ordered = False
            post = Post.query.all()               
        second_post = ""

    elif request.method == "POST" and 'searchinput' in request.form:
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



from wtforms import StringField, PasswordField, EmailField, SelectField,SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_wtf import FlaskForm
from website.model import User


class LoginForm(FlaskForm):
    username = StringField(
        label="الاسم", validators=[Length(min=6, max=40), DataRequired()]
    )
    password = PasswordField(
        label="كلمة السر", validators=[Length(min=6), DataRequired()]
    )
    submit = SubmitField(
        label = "تسجيل الدخول"
    )


class StudentRegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('هذا الاسم استخدم من قبل  . يرجي تغيير هذا الاسم ')


    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('هذا الايميل استخدم من قبل  . يرجي تغيير هذا الاسم ')
    
    def validate_password2(self, password2_to_check):
        if password2_to_check.data != self.password1.data :
            raise ValidationError("يجب ان يكون كلمة المرور و تاكيد كلمة المرور متساويان")
    
    username = StringField(
        label="الاسم", validators=[Length(min=6, max=40), DataRequired()]
    )
    password1 = PasswordField(
        label="كلمة السر", validators=[Length(min=6), DataRequired()]
    )
    password2 = PasswordField(
        label="تاكيد كلمة السر", validators=[DataRequired()]
    )
    email = EmailField(
        label="الايميل الاكتروني", validators=[DataRequired(), Length(min=8)]
    )
    schooltype = SelectField(label='اختار نوع مدرستك', choices=[('international', 'عالمية'), ('private', 'خاص'), ('public', 'عام'),
    ("language","لغات")])

    age = StringField(label = "العمر",validators=[Length(min=1,max=2), DataRequired()] )

    submit = SubmitField(
        label = "انشاء حساب"
    )


class TeacherRegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('هذا الاسم استخدم من قبل  . يرجي تغيير هذا الاسم ')


    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('هذا الايميل استخدم من قبل  . يرجي تغيير هذا الاسم ')
    
    def validate_password2(self, password2_to_check):
        if password2_to_check.data != self.password1.data :
            raise ValidationError("يجب ان يكون كلمة المرور و تاكيد كلمة المرور متساويان")
    



    username = StringField(
        label="الاسم", validators=[Length(min=6, max=40), DataRequired()]
    )
    email = EmailField(
        label="الايميل الاكتروني", validators=[DataRequired(), Length(min=8)]
    )
    password1 = PasswordField(
        label="كلمة السر", validators=[Length(min=6), DataRequired()]
    )
    password2 = PasswordField(
        label="تاكيد كلمة السر", validators=[DataRequired()]
    )
    
    first_subject = SelectField(
        label="المادة الاولى", choices=[('physics ', 'فيزياء'), ('chemistry', 'كيمياء'), ('biology', 'احياء'),
    ("arabic","العربية"), ("english", "الانجليزية"), ("french",  "الفرنسية"), ("italy","الايطالية "),
     ("physiologist", "فلسفة"), ("geography", "الجغرافيا"), ("history", "التاريخ"), ("math", "رياضيات")], validators=[DataRequired()]
    )
    second_subject = SelectField(
        label="المادة الثانية", choices=[ ("none", "لا شيء اخر"),('physics ', 'فيزياء'), ('chemistry', 'كيمياء'), ('biology', 'احياء'),
    ("arabic","العربية"), ("english", "الانجليزية"), ("french", "الفرنسية"), ("italy","الايطالية "),
     ("physiologist", "فلسفة"), ("geography", "الجغرافيا"), ("history", "التاريخ"), ("math", "رياضيات")]
    )
    submit = SubmitField(
        label = "انشاء حساب"
    )

class PostForm(FlaskForm):
    def validate_title(self, title_to_check):
        if self.create.data:
            if len(str(title_to_check.data)) < 6:
                raise ValidationError("لا يمكن انشاء سؤال ب عنوان اقل من ستة حروف")

    def validate_description(self, description_to_check):
        if self.create.data:
            if len(str(description_to_check.data)) < 20:
                raise ValidationError("لا يمكن انشاء سؤال بعلوملات غير كافية ف الموضوع")



    title = StringField(label="العنوان", validators=[Length(max=55)])
    description = TextAreaField(label="الموضوع" )
    subject = SelectField(label="نوع المادة", choices=[('physics ', 'فيزياء'), ('chemistry', 'كيمياء'), ('biology', 'احياء'),
    ("arabic","الغة العربية"), ("english", "الغةالانجليزية"), ("french", "الغة الفرنسية"), ("italy","الغة الايطالية "),
     ("physiologist", "فلسفة"), ("geography", "الجغرافيا"), ("history", "التاريخ"), ("math", "رياضيات")] )
    create = SubmitField(label="انشاء")
    cancel = SubmitField(label="اغلاق")



class UpdatePostForm(FlaskForm):
    description = TextAreaField(label="الموضوع" )
    subject = SelectField(label="نوع المادة", choices=[('physics ', 'فيزياء'), ('chemistry', 'كيمياء'), ('biology', 'احياء'),
    ("arabic","الغة العربية"), ("english", "الغةالانجليزية"), ("french", "الغة الفرنسية"), ("italy","الغة الايطالية "),
     ("physiologist", "فلسفة"), ("geography", "الجغرافيا"), ("history", "التاريخ"), ("math", "رياضيات")] )
    crt = SubmitField(label="تحديث")
    cal = SubmitField(label="اغلاق")
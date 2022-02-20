from tokenize import String
from wtforms import StringField, PasswordField, EmailField, SelectField,SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm


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
    username = StringField(
        label="الاسم", validators=[Length(min=6, max=40), DataRequired()]
    )
    password1 = PasswordField(
        label="كلمة السر", validators=[Length(min=6), DataRequired()]
    )
    password2 = PasswordField(
        label="تاكيد كلمة السر", validators=[EqualTo("password1"), DataRequired()]
    )
    email = EmailField(
        label="الايميل الاكتروني", validators=[Email(), DataRequired(), Length(min=8)]
    )
    schooltype = SelectField(label='اختار نوع مدرستك', choices=[('international', 'عالمية'), ('private', 'خاص'), ('public', 'عام'),
    ("language","لغات")])

    age = StringField(label = "العمر",validators=[Length(min=1,max=2), DataRequired()] )

    submit = SubmitField(
        label = "انشاء حساب"
    )


class TeacherRegisterForm(FlaskForm):
    username = StringField(
        label="الاسم", validators=[Length(min=6, max=40), DataRequired()]
    )
    email = EmailField(
        label="الايميل الاكتروني", validators=[Email(), DataRequired(), Length(min=8)]
    )
    password1 = PasswordField(
        label="كلمة السر", validators=[Length(min=6), DataRequired()]
    )
    password2 = PasswordField(
        label="تاكيد كلمة السر", validators=[EqualTo("password1"), DataRequired()]
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
    title = StringField(label="العنوان", validators=[Length(min=8 , max=100), DataRequired()])
    description = TextAreaField(label="الموضوع", validators=[Length(min=14), DataRequired()])
    subject = SelectField(label="نوع المادة", choices=[('physics ', 'فيزياء'), ('chemistry', 'كيمياء'), ('biology', 'احياء'),
    ("arabic","الغة العربية"), ("english", "الغةالانجليزية"), ("french", "الغة الفرنسية"), ("italy","الغة الايطالية "),
     ("physiologist", "فلسفة"), ("geography", "الجغرافيا"), ("history", "التاريخ"), ("math", "رياضيات")] , validators=[DataRequired()] )
    create = SubmitField(label="انشاء")
    cancel = SubmitField(label="حذف")
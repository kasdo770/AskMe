from wtforms import StringField, PasswordField, EmailField, RadioField,SubmitField
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
    schooltype = RadioField(
        label="نوع المدرسة", choices=[("language","الغات"), ("public","العام"), ("private","الخاص"), ("international","العالمية")]
    )
    submit = SubmitField(
        label = "انشاء حساب"
    )


class TeacherRegisterForm(FlaskForm):
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
    first_subject = StringField(
        label="المادة الاولة", validators=[Length(min=6, max=40), DataRequired()]
    )
    second_subject = StringField(
        label="المادة الثانية", validators=[Length(min=6, max=40)]
    )
    third_subject = StringField(
        label="المادة الثالثة", validators=[Length(min=6, max=40)]
    )
    submit = SubmitField(
        label = "انشاء حساب"
    )


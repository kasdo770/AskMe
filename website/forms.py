from wtforms import StringField, PasswordField, EmailField, SelectField,SubmitField
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
    password1 = PasswordField(
        label="كلمة السر", validators=[Length(min=6), DataRequired()]
    )
    password2 = PasswordField(
        label="تاكيد كلمة السر", validators=[EqualTo("password1"), DataRequired()]
    )
    email = EmailField(
        label="الايميل الاكتروني", validators=[Email(), DataRequired(), Length(min=8)]
    )
    submit = SubmitField(
        label = "انشاء حساب"
    )


from wtforms import StringField, PasswordField, EmailField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm


class StudentLoginForm(FlaskForm):
    username = StringField(
        label="Username", validators=[Length(min=6, max=40), DataRequired()]
    )
    password = PasswordField(
        label="Password", validators=[Length(min=6), DataRequired()]
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
        label="نوع المدرسة", choices=[("الغات"), ("العام"), ("الخاص"), ("العالمية")]
    )

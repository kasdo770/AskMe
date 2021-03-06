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
            raise ValidationError('هذا الايميل استخدم من قبل  . يرجي تغيير هذا الايميل ')
    
    def validate_password2(self, password2_to_check):
        if password2_to_check.data != self.password1.data :
            raise ValidationError("يجب ان يكونا كلمة المرور و تاكيد كلمة المرور متساويان")
    
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
    schooltype = SelectField(label='نوع المدرسة', choices=[('عالمية', 'عالمية'), ('خاص', 'خاص'), ('عام', 'عام'),
    ("لغات","لغات")])

    age = StringField(label = "العمر",validators=[Length(min=1,max=2), DataRequired()] )

    #gender = SelectField(label='الجنس', choices=[("ذكر", 'ذكر') , ('انثي', "انثي")])

    submit = SubmitField(
        label = "انشاء حساب"
    )

class AdminForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if not user:
            raise ValidationError('لا يوجد مستخدم بهذا الاسم')
    username = StringField(
        label="الاسم" 
    )
    submit = SubmitField(
        label="تم"
    )

class SupportForm(FlaskForm):
    def validate_description(self, description_to_check):
        if self.create.data:
            if len(str(description_to_check.data)) < 20:
                raise ValidationError("لا يمكنك انشاء سؤال بمعلومات غير كافية في الموضوع")

    def validate_title(self, title_to_check):
        if self.create.data:
            if len(str(title_to_check.data)) < 10:
                raise ValidationError("لا يمكنك انشاء سؤال بمعلومات غير كافية في العنوان")

    title = StringField(label="عنوان الطلب", validators=[Length(max=60),DataRequired()])
    description = TextAreaField(label="الموضوع", validators=[DataRequired()] )
    subjects =  SelectField(
        label="نوع طلبك", choices=[("'مشكلة في الحساب'",'مشكلة في الحساب'),("اقتراح","اقتراح"),('عطل فني','عطل فني')]
    )

    create = SubmitField(label="ارسال")
    cancel = SubmitField(label="اغلاق")


class TeacherRegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('هذا الاسم استخدم من قبل  . يرجي تغيير هذا الاسم ')


    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('هذا الايميل استخدم من قبل  . يرجي تغيير هذا الايميل ')
    
    def validate_password2(self, password2_to_check):
        if password2_to_check.data != self.password1.data :
            raise ValidationError("يجب ان يكونا كلمة المرور و تاكيد كلمة المرور متساويان")
    



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
        label="المادة الاولى", choices=[('فيزياء', 'فيزياء'), ('كيمياء', 'كيمياء'), ('احياء', 'احياء'),
    ("اللغة العربية","اللغة العربية"), ("اللغة الانجليزية", "اللغة الانجليزية"), ("اللغة الفرنسية", "اللغة الفرنسية"), ("اللغة الايطالية","اللغة الايطالية"),
     ("فلسفة", "فلسفة"), ("الجغرافيا", "الجغرافيا"), ("التاريخ", "التاريخ"), ("رياضيات", "رياضيات"), ("الحاسب الالي","الحاسب الالي")], validators=[DataRequired()]
    )
    second_subject = SelectField(
        label="المادة الثانية", choices=[("لا شيء اخر", "لا شيء اخر"),('فيزياء', 'فيزياء'), ('كيمياء', 'كيمياء'), ('احياء', 'احياء'),
    ("اللغة العربية","اللغة العربية"), ("اللغة الانجليزية", "اللغة الانجليزية"), ("اللغة الفرنسية", "اللغة الفرنسية"), ("اللغة الايطالية","اللغة الايطالية"),
     ("فلسفة", "فلسفة"), ("الجغرافيا", "الجغرافيا"), ("التاريخ", "التاريخ"), ("رياضيات", "رياضيات"),("الحاسب الالي","الحاسب الالي")]
    )
    #gender = SelectField(label='الجنس', choices=[("ذكر", 'male') , ('انثي', "female")])

    submit = SubmitField(
        label = "انشاء حساب"
    )

class PostForm(FlaskForm):
    def validate_title(self, title_to_check):
        if self.create.data:
            if len(str(title_to_check.data)) < 6:
                raise ValidationError("لا يمكن انشاء سؤال بعنوان اقل من ستة حروف")

    def validate_description(self, description_to_check):
        if self.create.data:
            if len(str(description_to_check.data)) < 20:
                raise ValidationError("لا يمكن انشاء سؤال بمعلومات غير كافية في الموضوع")


    title = StringField(label="العنوان", validators=[Length(max=60)])
    description = TextAreaField(label="الموضوع" )
    subject = SelectField(label="نوع المادة", choices=[('فيزياء', 'فيزياء'), ('كيمياء', 'كيمياء'), ('احياء', 'احياء'),
    ("اللغة العربية","اللغة العربية"), ("اللغة الانجليزية", "اللغة الانجليزية"), ("اللغة الفرنسية", "اللغة الفرنسية"), ("اللغة الايطالية","اللغة الايطالية"),
     ("فلسفة", "فلسفة"), ("الجغرافيا", "الجغرافيا"), ("التاريخ", "التاريخ"), ("رياضيات", "رياضيات"),("الحاسب الالي","الحاسب الالي")] )
    create = SubmitField(label="انشاء")
    cancel = SubmitField(label="اغلاق")



class UpdatePostForm(FlaskForm):
    description = TextAreaField(label="الموضوع" )
    subject = SelectField(label="نوع المادة", choices=[('فيزياء', 'فيزياء'), ('كيمياء', 'كيمياء'), ('احياء', 'احياء'),
    ("اللغة العربية","اللغة العربية"), ("اللغة الانجليزية", "اللغة الانجليزية"), ("اللغة الفرنسية", "اللغة الفرنسية"), ("اللغة الايطالية","اللغة الايطالية"),
     ("فلسفة", "فلسفة"), ("الجغرافيا", "الجغرافيا"), ("التاريخ", "التاريخ"), ("رياضيات", "رياضيات"),("الحاسب الالي","الحاسب الالي")] )
    crt = SubmitField(label="تحديث")
    cal = SubmitField(label="اغلاق")

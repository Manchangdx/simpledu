from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, 
     BooleanField, ValidationError, IntegerField, TextAreaField)
from wtforms.validators import (Length, Email, EqualTo, 
     DataRequired, URL, NumberRange)
from .models import User, db, Course

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, f):
        if User.query.filter_by(email=f.data).first():
            raise ValidationError('邮箱已经存在')

    def create_user(self):
        user = User()
        user.name = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    rm = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        u = User.query.filter_by(email=self.email.data).first()
        if u and not u.checkpassword(field.data):
            raise ValidationError('密码不对')

class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(5, 32)])
    description = TextAreaField('课程简介', 
        validators=[DataRequired(), Length(11, 256)])
    image_url = StringField('封面图片', validators=[DataRequired(), URL()])
    author_id = IntegerField('作者 ID', validators=[DataRequired(), 
        NumberRange(min=1, message='无效的用户 ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, f):
        if not User.query.get(f.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

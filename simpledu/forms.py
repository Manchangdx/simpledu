from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, DataRequired
from wtforms.validators import URL, NumberRange, ValidationError

from .models import db, User, Course, Live


class RegisterForm(FlaskForm):
    """用户注册表单类
    """

    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(),
            EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在。')
        if not field.data.isalnum():
            raise ValidationError('用户名只能由字母和数字组成，请重新输入。')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册。')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    """用户登录表单类
    """

    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户未注册。')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('用户密码错误。')


class CourseForm(FlaskForm):
    """创建课程表单类
    """

    name = StringField('课程名称', validators=[DataRequired(), Length(3, 24)])
    description = TextAreaField('课程简介', validators=[DataRequired(),
            Length(20, 256)])
    image_url = StringField('封面图片链接', validators=[DataRequired(), URL()])
    author_id = IntegerField('作者 ID', validators=[DataRequired(),
            NumberRange(min=1, message='无效的用户 ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('作者不存在，请输入正确的作者 ID 。')

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


class LiveForm(FlaskForm):
    """创建直播表单类
    """

    name = StringField('直播标题', validators=[DataRequired(), Length(3, 64)])
    description = TextAreaField('直播简介', validators=[DataRequired(),
            Length(20, 256)])
    user_id = IntegerField('直播用户 ID', validators=[DataRequired(),
            NumberRange(min=1, message='无效的用户 ID')])
    submit = SubmitField('提交')

    def validate_user_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('用户不存在，请输入正确的用户 ID 。')

    def create_live(self):
        live = Live()
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live

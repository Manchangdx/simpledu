from flask import Blueprint, render_template, flash, url_for, redirect
from flask import request, current_app
from flask_login import login_user, logout_user, login_required
from simpledu.models import db, Course, User, Test
from simpledu.forms import LoginForm, RegisterForm, TestForm

front = Blueprint('front', __name__)

@front.route('/test', methods=['get', 'post'])  # 这是测试用的函数
def test():
    form = TestForm()
    if form.validate_on_submit():
        test = Test()
        form.populate_obj(test)
        test.role = form.role.data
        db.session.add(test)
        db.session.commit()
        flash('添加 {} 成功'.format(test.name), 'success')
        print(test.role.value)
        print(type(test.role))
        form = TestForm()
    return render_template('test.html', form=form)

@front.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('index.html', pagination=pagination)

@front.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.rm.data)
        flash('Login Success', 'success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/register', methods=['get', 'post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('Register Success', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You 已经 logouted', 'info')
    return redirect(url_for('.index'))

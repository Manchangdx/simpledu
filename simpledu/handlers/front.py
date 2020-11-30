from flask import Blueprint, render_template, redirect, url_for, session
from flask import flash, current_app
from flask_login import login_required, login_user, logout_user

from simpledu.models import Course, User
from simpledu.forms import RegisterForm, LoginForm


front = Blueprint('front', __name__)


from flask import request, current_app


@front.route('/')
def index():
    """网站首页"""

    # 从请求对象中获取页数
    page = request.args.get('page', default=1, type=int)
    # 调用查询对象的 paginate 方法创建分页对象
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    # 最后将分页对象传入前端模板
    return render_template('index.html', pagination=pagination)


@front.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""

    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录。', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@front.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, form.remember_me.data)
        flash('登录成功。', 'success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录。', 'info')
    return redirect(url_for('.index'))

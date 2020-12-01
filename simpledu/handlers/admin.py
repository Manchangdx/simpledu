import json
from flask import Blueprint, render_template, request, current_app
from flask import redirect, url_for, flash

from ..decorators import admin_required
from ..models import db, Course, User, Live
from ..forms import CourseForm, RegisterForm, LiveForm, MessageForm
from .ws import redis


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    """后台管理主页"""

    return render_template('admin/index.html')


@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.order_by(Course.id.desc()).paginate(
            page = page,
            per_page = current_app.config['COURSES_PER_PAGE'],
            error_out = False
    )
    return render_template('admin/courses.html', pagination=pagination)


@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.order_by(User.id.desc()).paginate(
            page=page,
            per_page=current_app.config['USERS_PER_PAGE'],
            error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)


@admin.route('/lives')
@admin_required
def lives():
    page = request.args.get('page', default=1, type=int)
    pagination = Live.query.paginate(
            page=page,
            per_page=current_app.config['LIVES_PER_PAGE'],
            error_out=False
    )
    return render_template('admin/lives.html', pagination=pagination)


@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('成功创建课程：{}'.format(form.name.data), 'success')
        return redirect(url_for('.courses'))
    return render_template('admin/create_course.html', form=form)


@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('成功注册用户：{}'.format(form.username.data), 'success')
        return redirect(url_for('.users'))
    return render_template('admin/create_user.html', form=form)


@admin.route('/lives/create', methods=['GET', 'POST'])
@admin_required
def create_live():
    form = LiveForm()
    if form.validate_on_submit():
        form.create_live()
        flash('成功创建直播：{}'.format(form.name.data), 'success')
        return redirect(url_for('.lives'))
    return render_template('admin/create_live.html', form=form)


@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('成功修改课程：{}'.format(course.name), 'success')
        return redirect(url_for('.courses'))
    return render_template('admin/edit_course.html', course=course, form=form)


@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = RegisterForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            flash('用户 {} 的信息修改失败。'.format(user.username), 'info')
        else:
            flash('用户 {} 的信息修改成功。'.format(user.username), 'success')
            return redirect(url_for('.users'))
    return render_template('admin/edit_user.html', user=user, form=form)


@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('成功删除课程：{}'.format(course.name), 'warning')
    return redirect(url_for('.courses'))


@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('成功删除用户：{}'.format(user.username), 'warning')
    return redirect(url_for('.users'))


@admin.route('/message', methods=['GET', 'POST'])
@admin_required
def send_message():
    form = MessageForm()
    if form.validate_on_submit():
        data = {'username': 'System', 'text': form.text.data}
        redis.publish('chat', json.dumps(data))
        flash('系统消息发送成功', 'success')
        return redirect(url_for('.index'))
    return render_template('admin/send_message.html', form=form)

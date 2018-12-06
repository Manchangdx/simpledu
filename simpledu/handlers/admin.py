from flask import Blueprint, render_template, request, current_app
from flask import redirect, url_for, flash
from flask_login import current_user
from ..forms import CourseForm
from ..decorators import admin_required
from ..models import Course, User, db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
def haha():
    if not current_user.is_authenticated or current_user.role < User.ROLE_ADMIN:
        flash('你这个号级别不够', 'warning')
        return redirect(url_for('front.index'))

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/courses')
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page = page,
        per_page = current_app.config.get('ADMIN_PER_PAGE'),
        error_out = False
    )
    return render_template('admin/courses.html', pagination=pagination)

@admin.route('/courses/create', methods=['get', 'post'])
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功，课程名儿：{}'.format(form.name.data), 'success')
        return redirect(url_for('.courses'))
    return render_template('admin/create_course.html', form=form)

@admin.route('/courses/<int:course_id>/edit', methods=['get', 'post'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程更新成功了，课程名儿：{}'.format(course.name), 'success')
        return redirect(url_for('.courses'))
    return render_template('admin/edit_course.html', form=form, course=course)

@admin.route('/courses/<int:course_id>/delete')
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('该课程已删除~~', 'info')
    return redirect(url_for('.courses'))

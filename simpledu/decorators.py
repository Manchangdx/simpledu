from flask import abort, flash, redirect, url_for
from flask_login import current_user
from functools import wraps
from .models import User

def role_required(role):
    def haha(func):
        @wraps(func)
        def wrapper(*args, **kw):
            if not current_user.is_authenticated or current_user.role < role:
                flash('你这个号级别不够', 'warning')
                return redirect(url_for('front.index'))
            return func(*args, **kw)
        return wrapper
    return haha
            
staff_required = role_required(User.ROLE_STAFF)
admin_required = role_required(User.ROLE_ADMIN)

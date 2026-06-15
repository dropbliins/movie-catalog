from functools import wraps

from flask import abort
from flask_login import current_user

from extensions import login_manager


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapper

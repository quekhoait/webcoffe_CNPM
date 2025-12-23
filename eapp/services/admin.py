from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from eapp.models.Account import Role

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            # Chưa login → chuyển về login
            flash("Vui lòng đăng nhập để truy cập trang admin", "warning")
            return redirect(url_for('login'))
        if current_user.role != Role.STAFF:
            # Không phải admin → chặn truy cập
            flash("Bạn không có quyền truy cập trang này", "danger")
            return redirect(url_for('index'))  # hoặc trang khác
        return f(*args, **kwargs)
    return decorated_function

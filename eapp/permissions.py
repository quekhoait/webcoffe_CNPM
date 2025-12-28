from functools import wraps
from flask import flash, redirect, request, url_for
from flask_login import current_user
from eapp.models.Account import Role


def role_required(*roles : Role):
    def role_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Vui lòng đăng nhập để truy cập trang admin", "warning")
                return redirect(url_for('login',next=request.url))
            if current_user.role not in roles:
                flash("Bạn không có quyền truy cập trang này", "danger")
                return redirect(url_for('home')) 
            return f(*args, **kwargs)
        return decorated_function
    return role_decorator


admin_required = role_required(
    Role.ADMIN
)

staff_required = role_required(
    Role.STAFF
)
warehouse_required = role_required(
    Role.WAREHOUSE_KEEPER
)


cashier_required = role_required(
    Role.CASHIER
)

user_required = role_required(
    Role.USER,
    Role.STAFF,
    Role.CASHIER,
    Role.WAREHOUSE_KEEPER,
    Role.ADMIN
)
from app import login_required
from flask import Blueprint,render_template
from flask.ext.login import current_user

admin_staff = Blueprint('admin_staff', __name__, url_prefix='/admin')


@admin_staff.route('/home/')
@login_required(4)
def admin_home():
    user_info = {"username": current_user.username,
                 "email": current_user.email,
                 "role": current_user.role,
                 "status": current_user.status}
    return render_template('admin/confirmedLogIn.html', user_info=user_info)

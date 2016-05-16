from app import login_required
from flask import Blueprint,render_template, request
from flask.ext.login import current_user

from app.modules.common.models import AdminStaff, AdminDates

admin_staff = Blueprint('admin_staff', __name__, url_prefix='/admin')


@admin_staff.route('/home/')
@login_required(4)
def home():
    user_info = {"username": current_user.username,
                 "email": current_user.email,
                 "role": current_user.role,
                 "status": current_user.status}
    return render_template('admin/welcome.html', data=user_info)


@admin_staff.route('/set_dates/', methods=['GET', 'POST'])
@login_required(4)
def set_dates():
    staff = get_staff(current_user.get_id())
    date = get_date()
    user_info = {"username": current_user.username,
                 "type": staff.admin_type,
                 "email": current_user.email,
                 "role": current_user.role,
                 "status": current_user.status,
                 "dates": date}
    return render_template('admin/set_dates.html', data=user_info)


@admin_staff.route('/set_dates/save/', methods=['POST'])
@login_required(4)
def save():
    data = {}
    return render_template('admin/set_dates.html', data=data)


def get_staff(user_id):
    return AdminStaff.query.filter_by(user_id=user_id).first()

def get_date():
    return AdminDates.query.all()
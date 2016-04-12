from app import login_required
from flask import Blueprint

admin_staff = Blueprint('admin_staff', __name__, url_prefix='/admin')


@admin_staff.route('/home/')
@login_required(4)
def home():
    return 'Admin Home'

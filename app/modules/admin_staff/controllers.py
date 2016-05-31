from datetime import datetime

from app import login_required, db
from app.modules.common.controllers import passchange
from flask import Blueprint, render_template, request, flash
from flask.ext.login import current_user
from flask import url_for

from app.modules.common.models import AdminStaff, AdminDates, Year, StudyGroup, Semester, Student

admin_staff = Blueprint('admin_staff', __name__, url_prefix='/admin')


@admin_staff.route('/home/')
@login_required(4)
def home():
    user_info = {"username": current_user.username,
                 "email": current_user.email,
                 "role": current_user.role,
                 "status": current_user.status}
    return render_template('admin/welcome.html', data=user_info)


@admin_staff.route('/settings/', methods=['GET', 'POST'])
@login_required(4)
def settings():
    data = {"username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            "status": current_user.status}

    template = 'admin/settings.html'
    route = 'admin_staff.settings'

    return passchange(data, request, template, route)


@admin_staff.route('/set_dates/', methods=['GET'])
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


@admin_staff.route('/set_dates/', methods=['POST'])
@login_required(4)
def save():
    for element in request.json:
        type_section = element['type']
        from_date = element["from"]
        to_date = element["to"]
        __save_date(type_section, from_date, to_date)
    return url_for('admin_staff.set_dates')


@admin_staff.route('/list_students/', methods=['GET', 'POST'])
@login_required(4)
def list_students():
    data = {}
    template = 'admin/list_students.html'

    data['years'] = Year.query.all()
    data['selected_year'] = ''
    data['groups'] = StudyGroup.query.all()
    data['selected_group'] = ''
    data['students'] = Student.query.all()

    for student in data['students']:
        # TODO compute each students average mark for that year
        student.mark = 10

    if request.method == 'POST':
        selected_year = request.form.get('year-select', '')
        if selected_year != '':
            selected_year = int(selected_year)

        selected_group = request.form.get('group-select', '')
        if selected_group != '':
            selected_group = int(selected_group)

        data['selected_year'] = selected_year
        data['selected_group'] = selected_group

    return render_template(template, data=data)


@admin_staff.route('/crud_students/', methods=['GET', 'POST'])
@login_required(4)
def crud_students():
    groups = StudyGroup.query.all()
    groups = list(map(lambda group: {"id": group.id, "value": group.group_number}, groups))

    data = {"username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            "status": current_user.status,
            "groups": groups}
    return render_template("admin/crud_students.html", data=data)


def __save_date(section, from_date, to_date):
    if section is not "" or section is None:
        AdminDates.query.filter_by(type=int(section)).update(dict(from_date=from_date, to=to_date))
        db.session.commit()


def get_staff(user_id):
    return AdminStaff.query.filter_by(user_id=user_id).first()


def get_date():
    return AdminDates.query.all()

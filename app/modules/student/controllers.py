from app import login_required, db
from flask import Blueprint, render_template
from flask.ext.login import current_user

from app.modules.common.models import Student

student = Blueprint('student', __name__, url_prefix='/student')


@student.route('/home/')
@login_required(1)
def home():
    data = {"username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            }
    return render_template('student/welcome.html', data=data)


@student.route('/grades/temporary/', methods=['GET', 'POST'])
@login_required(1)
def grades_temporary():
    stud = Student.query.filter_by(user_id=current_user.id).first()
    data = {
        "firstname": stud.first_name,
        "lastname": stud.last_name
    }
    return render_template('student/temporary_grades.html', data=data)


@student.route('/grades/final/', methods=['GET', 'POST'])
@login_required(1)
def grades_final():
    stud = Student.query.filter_by(user_id=current_user.id).first()
    data = {
        "firstname": stud.first_name,
        "lastname": stud.last_name,
    }
    return render_template('student/final_grades.html', data=data)

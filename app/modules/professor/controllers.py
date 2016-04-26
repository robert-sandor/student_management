from app import login_required
from app.modules.common.models import Professor, ProfessorRole, Course
from flask import Blueprint, render_template
from flask_login import current_user

professor = Blueprint('professor', __name__, url_prefix='/prof')


@professor.route('/home/')
@login_required(2)
def home():
    current_proffesor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = []
    for professor_roles in current_proffesor.professor_roles:
        if professor_roles.role_type.id == 1:
            courses.append(professor_roles.course.course_name)
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email,
            "courses": courses}

    return render_template("professor/professor.html", data=data)




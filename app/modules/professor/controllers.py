from app import login_required
from app.modules.common.models import Professor, ProfessorRole, Course
from flask import Blueprint, render_template
from flask_login import current_user

professor = Blueprint('professor', __name__, url_prefix='/prof')


@professor.route('/home/', methods=['GET'])
@login_required(2)
def home():
    current_proffesor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_courses_for_professor(current_proffesor)
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email,
            "courses": courses}

    return render_template("professor/professor.html", data=data)


@professor.route('/grading/<course>', methods=['GET'])
@login_required(2)
def get_students_for_course(course):
    current_proffesor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_courses_for_professor(current_proffesor)

    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email,
            "courses": courses, "content": course}

    return render_template("professor/professor.html", data=data)


def __get_courses_for_professor(professor):
    return [professor_role.course.course_name for professor_role in professor.professor_roles if professor_role.role_type.id == 1]

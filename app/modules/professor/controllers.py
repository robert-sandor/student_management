from app import login_required
from app.modules.common.models import Professor, ProfessorRole, Course
from flask import Blueprint, render_template
from flask_login import current_user

professor_blueprint = Blueprint('professor', __name__, url_prefix='/prof')


@professor_blueprint.route('/home/', methods=['GET'])
@login_required(2)
def home():
    professor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_professor_courses(professor)
    courses_names = __get_courses_names(courses)
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email,
            "courses_names": courses_names}

    return render_template("professor/welcome.html", data=data)


@professor_blueprint.route('/grading/<course>', methods=['GET'])
@login_required(2)
def get_students_for_course(course):
    current_proffesor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_professor_courses(current_proffesor)
    courses_names = __get_courses_names(courses)
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email,
            "courses_names": courses_names, "content": course}

    return render_template("professor/grading.html", data=data)


def __get_professor_courses(professor) -> [Course]:
    return [professor_role.course for professor_role in professor.professor_roles if professor_role.role_type.id == 1]


def __get_courses_names(courses) -> [str]:
    return [course.course_name for course in courses]

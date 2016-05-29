from app import login_required, db
from app.modules.common.controllers import passchange
from app.modules.common.models import OptionalCourse, Course, Package, Professor, GradeEvaluation
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import current_user

professor_cod = Blueprint('professor_cod', __name__, url_prefix='/prof_cod')


@professor_cod.route('/home/')
@login_required(3)
def home():
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email}
    return render_template("professor_cod/professor_cod.html", data=data)


@professor_cod.route('/proposals/')
@login_required(3)
def proposals():
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email}
    optional_courses = OptionalCourse.query.all()
    courses = []
    for optional_course in optional_courses:
        courses.append(optional_course.course)
    data["opts"] = optional_courses
    data["proposals"] = courses
    data["packages"] = Package.query.all()
    return render_template("professor_cod/proposals.html", data=data)

@professor_cod.route('/settings/', methods=['GET', 'POST'])
@login_required(3)
def settings():
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email}
    template = 'professor_cod/settings.html'
    route = 'professor_cod.settings'

    return passchange(data, request, template, route)

@professor_cod.route('/proposals/save/', methods=['POST'])
@login_required(3)
def save():
    data = {}
    for pack in request.json.keys():
        pack_name = Package.query.filter_by(id=int(pack)).first().name
        courses = request.json[pack]
        for course_id in courses:
            OptionalCourse.query.filter_by(course_id=int(course_id)).update(dict(package_id=int(pack)))
            db.session.commit()
    return url_for('professor_cod.home')


@professor_cod.route('/grading/<course_id>', methods=['GET'])
@login_required(3)
def get_students_for_course(course_id):
    current_proffesor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_professor_courses(current_proffesor)
    students = []
    selected_course = None
    for course in courses:
        if course.id == int(float(course_id)):
            selected_course = course
            for evaluation in course.evaluation:
                student = evaluation.contract.student
                grades = list([{"grade": grade.grade, "date": grade.evaluation_date, "id": grade.id} for grade in
                               evaluation.grades])
                final_grade = max(grades, key=lambda x: x["grade"] if x["grade"] else 0)["grade"] if grades else 0
                students.append({"student": student, "grades": grades, "final_grade": final_grade})
    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "courses": courses,
            "selected_course": selected_course,
            "students": students}

    return render_template("professor_cod/grading.html", data=data)


@professor_cod.route('/prof_cod/grading/', methods=['POST'])
@login_required(3)
def save_grade():
    print(request.json)
    course_id = 1
    for element in request.json:
        course_id = element["course_id"]
        # course = Course.query.get(int(course_id))
        # student_id = element["student_id"]
        # student = Student.query.get(int(student_id))
        grade_1_id = int(element["grade_1"]["id"])
        grade_1_value = element["grade_1"]["value"]
        grade_2_id = int(element["grade_2"]["id"])
        grade_2_value = element["grade_2"]["value"]
        grade_3_id = int(element["grade_3"]["id"])
        grade_3_value = element["grade_3"]["value"]
        __save_grade(grade_1_id, grade_1_value)
        __save_grade(grade_2_id, grade_2_value)
        __save_grade(grade_3_id, grade_3_value)

    return url_for('prof_cod.get_students_for_course', course_id=course_id)


def __save_grade(grade_id, value):
    if value is not "" or value is None:
        GradeEvaluation.query.filter_by(id=grade_id).update(dict(grade=int(value)))
        db.session.commit()


def __get_professor_courses(professor) -> [Course]:
    return [professor_role.course for professor_role in professor.professor_roles if professor_role.role_type.id == 1]


def __get_courses_names(courses) -> [str]:
    return [course.course_name for course in courses]
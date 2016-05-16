from app import login_required, db
from app.modules.common.models import Professor, Course, Student, GradeEvaluation
from flask import Blueprint, render_template, request, url_for
from flask_login import current_user

professor_blueprint = Blueprint('professor', __name__, url_prefix='/prof')


@professor_blueprint.route('/home/', methods=['GET'])
@login_required(2)
def home():
    professor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_professor_courses(professor)
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email,
            "selected_course": None, "courses": courses}

    return render_template("professor/welcome.html", data=data)


@professor_blueprint.route('/grading/<course_id>', methods=['GET'])
@login_required(2)
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
                grades = list([(grade.grade, grade.evaluation_date, grade.id) for grade in evaluation.grades])
                final_grade = max(grades, key=lambda x: x[0] if x[0] else 0)[0] if grades else 0
                students.append({"student": student, "grades": grades, "final_grade": final_grade})
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email,
            "courses": courses, "selected_course": selected_course, "students": students}

    return render_template("professor/grading.html", data=data)


@professor_blueprint.route('/professor/grading/', methods=['POST'])
@login_required(2)
def save():
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

    return url_for('professor.get_students_for_course', course_id=course_id)


def __save_grade(grade_id, value):
    if value is not "" or value is None:
        print("-" + value + "-")
        GradeEvaluation.query.filter_by(id=grade_id).update(dict(grade=int(value)))
        db.session.commit()



def __get_professor_courses(professor) -> [Course]:
    return [professor_role.course for professor_role in professor.professor_roles if professor_role.role_type.id == 1]


def __get_courses_names(courses) -> [str]:
    return [course.course_name for course in courses]

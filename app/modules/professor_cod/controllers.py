from app import login_required, db
from app.modules.common.models import OptionalCourse, Course, Package, Professor, GradeEvaluation, ProposedCourses, \
    Semester
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import current_user
from random import random, randint

professor_cod = Blueprint('professor_cod', __name__, url_prefix='/prof_cod')


@professor_cod.route('/home/')
@login_required(3)
def home():
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email}
    return render_template("professor_cod/professor_cod.html", data=data)


@professor_cod.route('/proposals/')
@login_required(3)
def proposals():
    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "proposals": ProposedCourses.query.all(),
            "packages": Package.query.all(),
            "profs": Professor.query.all(),
            "semesters": Semester.query.all(),
            }
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
    for course in request.json.keys():
        # Get the corresponding course
        proposed_course = ProposedCourses.query.filter_by(id=int(course)).first()
        # Creating course, main entry in Courses table
        # Course name and description setting
        course_name = proposed_course.course_name
        # Needs to be shortened since our course supports only 200 chars
        course_description = proposed_course.description[:199]
        # Generating some type of course code, todo: maybe better implementation?
        course_code = str(proposed_course.speciality[0]).upper() + str(proposed_course.speciality[0]).upper() + str(
                          randint(1000, 9999))
        # Get data about professor and semester
        collected_data = request.json[course]
        p = Professor.query.filter_by(id=collected_data['prof']).first()
        last_semester = Semester.query.filter_by(id=collected_data['sem']).first()
        # For credits set a default of 6
        course_credits = int(collected_data['credits'])
        # For eval type set a default of C
        eval_type = collected_data['eval']
        # Create course from give data
        # Settings name as username, seeing as we don't have an ACTUAL name on the prof
        highest_id = db.session.query(Course).order_by(Course.id.desc()).first().id + 1
        c = Course(id=highest_id, course_name=course_name, course_description=course_description,
                   code=course_code, professor_name=p.auth_user.username, credits=course_credits,
                   evaluation_type=eval_type, is_optional=True)
        c.semester = last_semester
        db.session.add(c)
        db.session.commit()
        # Creating course, optional entry, in OptionalCourses table
        # Setting of package and language, available directly on proposed course
        package = collected_data['package']
        language = proposed_course.study_line
        # Get latest course added
        c = db.session.query(Course).order_by(Course.id.desc()).first()
        # Get the departament using the professor assigned
        dept = p.department
        oc = OptionalCourse(course_id=c.id, active=False, id_department=dept.id,
                            package_id=package, course_language=language)

        db.session.add(oc)
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

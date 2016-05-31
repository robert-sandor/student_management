from datetime import datetime

from app import login_required, db
from app.modules.common.controllers import passchange
from app.modules.common.models import OptionalCourse, Course, Package, Professor, GradeEvaluation, ProposedCourses, \
    Semester, ProfessorRole, AdminDates, Student, Evaluation
from collections import defaultdict
from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
from random import randint

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
        # Set credits
        course_credits = int(collected_data['credits'])
        # Set eval type
        eval_type = collected_data['eval']

        # Setting language, available directly on proposed course
        language = proposed_course.study_line

        # Create course from give data
        # Settings name as username, seeing as we don't have an ACTUAL name on the prof yet
        highest_id = db.session.query(Course).order_by(Course.id.desc()).first().id + 1
        c = Course(id=highest_id, course_name=course_name, course_description=course_description,
                   code=course_code, professor_name=p.auth_user.username, credits=course_credits,
                   evaluation_type=eval_type, is_optional=True, course_language=language)
        c.semester = last_semester
        db.session.add(c)
        db.session.commit()
        # Creating course, optional entry, in OptionalCourses table
        # Setting of package, available directly on proposed course
        package = collected_data['package']
        # Get latest course added
        c = db.session.query(Course).order_by(Course.id.desc()).first()
        # Get the departament using the professor assigned
        dept = p.department
        oc = OptionalCourse(course_id=c.id, active=False, id_department=dept.id,
                            package_id=package)

        db.session.add(oc)
        # Correlate professor with created course
        pc = ProfessorRole(professor_id=p.id, course_id=c.id, role_type_id=1)
        db.session.add(pc)
        db.session.commit()
    return url_for('professor_cod.home')


@professor_cod.route('/grading/<course_id>', methods=['GET'])
@login_required(3)
def get_students_for_course(course_id):
    current_proffesor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_professor_courses(current_proffesor)
    students = []
    selected_course = None
    students_dict = defaultdict(list)
    for course in courses:
        if course.id == int(float(course_id)):
            selected_course = course
            for evaluation in course.evaluation:
                contract = evaluation.contract
                student = contract.student
                group = student.semigroup.study_group
                grades = list([{"grade": grade.grade,
                                "date": grade.evaluation_date if grade.evaluation_date else datetime.min.date(),
                                "id": grade.id} for indx, grade in
                               enumerate(evaluation.grades)])
                final_grade = max(grades, key=lambda x: x["grade"] if x["grade"] else 0)["grade"] if grades else 0
                students.append(
                    {"student": student, "contract": contract.id, "group": group.group_number, "grades": grades,
                     "final_grade": final_grade})
    for student in students:
        students_dict[student["group"]].append(student)
    session_dates = __get_session_date()
    retake_dates = __get_retake_date()
    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "courses": courses,
            "rank_prof": current_proffesor.rank,
            "min_date": datetime.min.date(),
            "date_now": datetime.now().date(),
            "session_dates": session_dates,
            "retake_dates": retake_dates,
            "selected_course": selected_course,
            "students_dict": students_dict}

    return render_template("professor_cod/grading.html", data=data)


@professor_cod.route('/prof_cod/grading/', methods=['POST'])
@login_required(3)
def save_grade():
    course_id = 1
    group_dates = request.json["group_dates"]
    group_dates_dict = {}
    for pair in group_dates:
        group = int(pair["group"])
        dates = pair["dates"]
        dates_dict = {}
        for elem in dates:
            dates_dict[elem["grade"][0]] = elem["grade"][1]
        group_dates_dict[group] = dates_dict
    for element in request.json["students"]:
        course_id = element["course_id"]
        student_id = element["student_id"]
        group_number = int(__get_student_group(student_id))
        grade_1_id = int(element["grade_1"]["id"])
        grade_1_value = element["grade_1"]["value"]
        grade_2_id = int(element["grade_2"]["id"])
        grade_2_value = element["grade_2"]["value"]
        grade_3_id = int(element["grade_3"]["id"])
        grade_3_value = element["grade_3"]["value"]
        __save_grade(grade_1_id, grade_1_value, group_dates_dict[group_number][0])
        __save_grade(grade_2_id, grade_2_value, group_dates_dict[group_number][1])
        __save_grade(grade_3_id, grade_3_value, group_dates_dict[group_number][2])
        __check_if_passed(grade_1_value, grade_2_value, grade_3_value, __get_evaluation_from_grade(grade_1_id))

    return url_for('prof_cod.get_students_for_course', course_id=course_id)


def __get_session_date():
    admin_date = AdminDates.query.filter_by(id=1).first()
    return admin_date.from_date, admin_date.to


def __get_retake_date():
    admin_date = AdminDates.query.filter_by(id=2).first()
    return admin_date.from_date, admin_date.to


def __save_grade(grade_id, value, date):
    if date is not " " and date is not None and date is not "":
        c_date = datetime.strptime(date + " 00:00", '%d/%m/%Y %H:%M').date()
        GradeEvaluation.query.filter_by(id=grade_id).update(dict(evaluation_date=c_date))
        db.session.commit()
    if value is not "" and value is not None and not value == "absent":
        GradeEvaluation.query.filter_by(id=grade_id).update(dict(grade=int(value), present=True))
        db.session.commit()


def __get_professor_courses(professor) -> [Course]:
    return [professor_role.course for professor_role in professor.professor_roles if professor_role.role_type.id == 1]


def __get_courses_names(courses) -> [str]:
    return [course.course_name for course in courses]


def __get_student_group(student_id) -> int:
    return Student.query.filter_by(id=student_id).first().semigroup.study_group.group_number


def __get_evaluation_from_grade(grade_id) -> Evaluation:
    return GradeEvaluation.query.filter_by(id=grade_id).first().course


def __check_if_passed(grade_1, grade_2, grade_3, evaluation: Evaluation):
    grades = [grade_1, grade_2, grade_3]
    grades = list(filter(lambda grade: grade is not "" and grade is not None and not grade == "absent" and int(grade) >= 5, grades))
    if len(grades) > 0:
        evaluation._pass = True
        db.session.commit()


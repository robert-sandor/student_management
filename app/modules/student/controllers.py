from app.modules.common.controllers import passchange
from sqlalchemy import func

from app import login_required, db
from flask import Blueprint, render_template, request
from flask.ext.login import current_user

from app.modules.common.models import *


student = Blueprint('student', __name__, url_prefix='/student')


@student.route('/home/')
@login_required(1)
def home():
    data = {"username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            }
    return render_template('student/welcome.html', data=data)


@student.route('/settings/', methods=['GET', 'POST'])
@login_required(1)
def settings():
    data = {"username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            }

    template = 'student/settings.html'
    route = 'student.settings'

    return passchange(data, request, template, route)


@student.route('/grades/temporary/', methods=['GET', 'POST'])
@login_required(1)
def grades_temporary():
    student = get_student(current_user.get_id())
    courses = []
    for contract in student.contract:
        for evaluation in contract.evaluation:
            course = get_course(evaluation.course_id)
            grades = list([{"grade": grade.grade, "date": grade.evaluation_date, "id": grade.id} for grade in
                               evaluation.grades])
            final_grade = max(grades, key=lambda x: x["grade"] if x["grade"] else 0) if grades else 0
            courses.append({"course": course.course_name, "grades": grades, "final_grade": final_grade})
    data = {"username": current_user.username,
            "role": current_user.role,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": current_user.email,
            "courses": courses
            }
    return render_template('student/temporary_grades.html', data=data)


@student.route('/grades/final/', methods=['GET', 'POST'])
@login_required(1)
def grades_final():
    student = get_student(current_user.get_id())
    courses = []
    for contract in student.contract:
        for evaluation in contract.evaluation:
            course = get_course(evaluation.course_id)
            grades = list([{"grade": grade.grade, "date": grade.evaluation_date, "id": grade.id} for grade in
                               evaluation.grades])
            final_grade = max(grades, key=lambda x: x["grade"] if x["grade"] else 0) if grades else 0
            courses.append({"course": course.course_name, "grades": grades, "final_grade": final_grade})
    data = {"username": current_user.username,
            "role": current_user.role,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": current_user.email,
            "courses": courses
            }
    return render_template('student/final_grades.html', data=data)


@student.route('/contracts/add_contract/')
@login_required(1)
def add_contract():
    current_student = get_student(current_user.id)

    semigroup = current_student.semigroup
    group = semigroup.study_group
    semester = group.semester
    year = semester.year
    study_plan = year.study_plan
    study_line = study_plan.study_line
    specialty = study_line.specialty
    study_level = specialty.study_level
    faculty = study_level.faculty

    semester_id = semester.id
    semesters = []

    years = Year.query.filter_by(study_plan_id=study_plan.id).all()
    for y in years:
        s = Semester.query.filter_by(year_id=y.id).all()
        for sem in s:
            semesters.append({"id": sem.id, "year_id": sem.year_id,
                              "semester": (y.study_year-1)*2 + sem.semester})

    # courses = {sem.semester: [] for sem in semesters}
    packages = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    courses = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    optional_courses = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    pkges = Package.query.all()
    for sem in semesters:
        c = Course.query.filter_by(semester_id=sem['id']).all()
        for course in c:
            if course.is_optional:
                opt_c = OptionalCourse.query.filter_by(course_id=course.id).first()
                package = Package.query.filter_by(id=opt_c.package_id).first()
                packages[opt_c.package_id].append({"course_name": course.course_name,
                                                    "course_description": course.course_description,
                                                    "code": course.code,
                                                    "professor_name": course.professor_name,
                                                    "credits": course.credits,
                                                    "evaluation_type": course.evaluation_type,
                                                    "course_language": course.course_language,
                                                    "package_id": opt_c.package_id,
                                                    "package_name": package.name,
                                                    "semester_nr": sem['semester']
                                                    })

                optional_courses[sem['semester']].append({"course_name": course.course_name,
                                                          "course_description": course.course_description,
                                                          "code": course.code,
                                                          "professor_name": course.professor_name,
                                                          "credits": course.credits,
                                                          "evaluation_type": course.evaluation_type,
                                                          "course_language": course.course_language,
                                                          "package_id": opt_c.package_id,
                                                          "package_name": package.name
                                                          })
            else:
                courses[sem['semester']].append({"course_name": course.course_name,
                                            "course_description": course.course_description,
                                            "code": course.code,
                                            "professor_name": course.professor_name,
                                            "credits": course.credits,
                                            "evaluation_type": course.evaluation_type,
                                            "course_language": course.course_language,
                                            "is_optional": course.is_optional})
    data = {"username": current_user.username,
            "role": current_user.role,
            "first_name": current_student.first_name,
            "last_name": current_student.last_name,
            "email": current_user.email,
            "semesters": semesters,
            "courses": courses,
            "packages": packages
            }

    return render_template("student/add_contract.html", data=data)


def get_student(user_id):
    return Student.query.filter_by(user_id=user_id).first()


def get_contract(student):
    return Contract.query.filter_by(student_id=student.id).first()


def get_evaluation(contract) -> [Evaluation]:
    return db.session.query(Evaluation).filter(Contract.student, Evaluation.contract, Evaluation.course).filter_by(contract_id=contract.id).first()


def get_course(course_id) -> [Course]:
    return Course.query.filter_by(id=course_id).first()


def get_grade_evaluation(contract) -> [GradeEvaluation]:
    return db.session.query(GradeEvaluation).filter(Evaluation.course, Evaluation.contract, GradeEvaluation.course).filter_by(contract_id=contract.id).all()


def get_final_evaluation(contract) -> [GradeEvaluation]:
    return db.session.query(GradeEvaluation.evaluation_date, func.max(GradeEvaluation.grade).label('max_grade')).group_by(GradeEvaluation.grade).group_by(GradeEvaluation.evaluation_date).filter(Evaluation.course,
        Evaluation.contract, GradeEvaluation.course).filter_by(contract_id=contract.id).first()


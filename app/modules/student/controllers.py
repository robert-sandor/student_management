from sqlalchemy import func

from app import login_required, db
from flask import Blueprint, render_template
from flask.ext.login import current_user

from app.modules.common.models import Student, Contract, GradeEvaluation, Course, Evaluation

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


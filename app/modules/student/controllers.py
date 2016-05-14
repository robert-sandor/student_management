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
    eval = get_evaluation(get_contract(student))
    grade_eval = get_grade_evaluation(get_contract(student))
    grades, dates = [], []
    for grade in grade_eval:
        if not grade.present: grades.append("Absent")
        else: grades.append(grade.grade)
        dates.append(grade.evaluation_date)
    data = [{"username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            "course": get_course_name(eval.course_id).course_name,
            "firstname": student.first_name,
            "lastname": student.last_name,
            "grades": grades,
            "dates": dates
            }]
    return render_template('student/temporary_grades.html', data=data)


@student.route('/grades/final/', methods=['GET', 'POST'])
@login_required(1)
def grades_final():
    student = get_student(current_user.get_id())
    contract = get_contract(student)
    eval = get_evaluation(contract)
    # grade_eval = get_grade_evaluation(contract)
    grade_eval = get_final_evaluation(contract)
    print("fsafasdas", grade_eval)
    data = { "role": current_user.role,
            "firstdate": grade_eval.evaluation_date,
            "firstgrade": grade_eval.max_grade,
            "passed": eval._pass,
            "course": get_course_name(eval.course_id).course_name,
            "firstname": student.first_name,
            "lastname": student.last_name,
            "username": current_user.username
            }
    return render_template('student/final_grades.html', data=data)


def get_student(user_id):
    return Student.query.filter_by(user_id=user_id).first()


def get_contract(student):
    return Contract.query.filter_by(student_id=student.id).first()


def get_evaluation(contract) -> [Evaluation]:
    return db.session.query(Evaluation).filter(Contract.student, Evaluation.contract, Evaluation.course).filter_by(contract_id=contract.id).first()


def get_course_name(course_id) -> [Course]:
    return Course.query.filter_by(id=course_id).first()


def get_grade_evaluation(contract) -> [GradeEvaluation]:
    return db.session.query(GradeEvaluation).filter(Evaluation.course, Evaluation.contract, GradeEvaluation.course).filter_by(contract_id=contract.id).all()


def get_final_evaluation(contract) -> [GradeEvaluation]:
    return db.session.query(GradeEvaluation.evaluation_date, func.max(GradeEvaluation.grade).label('max_grade')).group_by(GradeEvaluation.grade).group_by(GradeEvaluation.evaluation_date).filter(Evaluation.course,
        Evaluation.contract, GradeEvaluation.course).filter_by(contract_id=contract.id).first()


from app import login_required, db
from app.modules.common.controllers import passchange
from app.modules.common.forms import PasswdChangeForm
from app.modules.common.models import Course, GradeEvaluation, Student, AdminDates, Professor, ProposedCourses, \
    Evaluation
from app.modules.professor.forms import ProposalForm
from config import SQLALCHEMY_DATABASE_URI
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
from datetime import datetime

professor_blueprint = Blueprint('professor', __name__, url_prefix='/prof')

ranks = {"doctorand": 0,
         "asistent": 1,
         "conferentiar": 2,
         "lector": 3,
         "prof": 4}


@professor_blueprint.route('/home/', methods=['GET'])
@login_required(2)
def home():
    professor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_professor_courses(professor)

    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "selected_course": None,
            "courses": courses,
            "rank_prof": professor.rank,
            "ranks": ranks}
    return render_template("professor/professor.html", data=data)


@professor_blueprint.route('/settings/', methods=['GET', 'POST'])
@login_required(2)
def settings():
    professor = Professor.query.filter_by(id_user=current_user.get_id()).first()
    courses = __get_professor_courses(professor)

    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "selected_course": None,
            "courses": courses,
            "rank_prof": professor.rank,
            "ranks": ranks}

    template = 'professor/settings.html'
    route = 'professor.settings'

    return passchange(data, request, template, route)


@professor_blueprint.route('/proposals/add_proposal/', methods=['GET', 'POST'])
@login_required(2)
def add_proposal():
    prof = Professor.query.filter_by(id_user=current_user.id).first()
    proposed_courses = ProposedCourses.query.filter_by(professor_id=prof.id).all()
    form = ProposalForm(request.form)

    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "rank_prof": prof.rank,
            "ranks": ranks,
            "no_proposals": proposed_courses.__len__(),
            "max_proposals": 2}

    if form.validate_on_submit():
        proposal = ProposedCourses(prof.id, form.course_name.data, form.speciality.data, form.study_line.data,
                                   form.description.data)
        form.course_name.data = ""
        form.speciality.data = ""
        form.study_line.data = ""
        form.description.data = ""

        db.session.add(proposal)
        db.session.commit()

    return render_template("professor/add_proposal.html", data=data, form=form)


@professor_blueprint.route('/proposals/view_proposals/')
@login_required(2)
def view_proposals():
    prof = Professor.query.filter_by(id_user=current_user.id).first()
    courses = __get_professor_courses(prof)
    proposed_courses = ProposedCourses.query.filter_by(professor_id=prof.id).all()
    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "rank_prof": prof.rank,
            "ranks": ranks,
            "no_proposals": proposed_courses.__len__(),
            "max_proposals": 2,
            "proposals": proposed_courses,
            "courses": courses}
    return render_template("professor/view_proposals.html", data=data)


@professor_blueprint.route('/grading/<course_id>', methods=['GET'])
@login_required(2)
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
                grades = list([{"grade": grade.grade, "date": grade.evaluation_date if grade.evaluation_date else datetime.min.date(), "id": grade.id} for indx, grade in
                               enumerate(evaluation.grades)])
                final_grade = max(grades, key=lambda x: x["grade"] if x["grade"] else 0)["grade"] if grades else 0
                students.append({"student": student, "contract": contract.id, "group": group.group_number,  "grades": grades, "final_grade": final_grade})
    for student in students:
        students_dict[student["group"]].append(student)
    session_dates = __get_session_date()
    retake_dates = __get_retake_date()
    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "courses": courses,
            "rank_prof": current_proffesor.rank,
            "ranks": ranks,
            "min_date": datetime.min.date(),
            "date_now": datetime.now().date(),
            "session_dates": session_dates,
            "retake_dates": retake_dates,
            "selected_course": selected_course,
            "students_dict": students_dict}

    return render_template("professor/grading.html", data=data)


@professor_blueprint.route('/professor/grading/', methods=['POST'])
@login_required(2)
def save():
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

    return url_for('professor.get_students_for_course', course_id=course_id)


@professor_blueprint.route('/proposals/update_proposal/', methods=['GET', 'POST'])
@professor_blueprint.route('/proposals/update_proposal/<proposal_id>/', methods=['GET', 'POST'])
@login_required(2)
def update_proposal(proposal_id=None):
    if proposal_id is None:
        return redirect(url_for('404'))
    prof = Professor.query.filter_by(id_user=current_user.id).first()
    proposed_courses = ProposedCourses.query.filter_by(professor_id=prof.id).all()
    proposed_course = ProposedCourses.query.filter_by(id=proposal_id).first()
    form = ProposalForm(request.form)

    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "rank_prof": prof.rank,
            "ranks": ranks,
            "no_proposals": proposed_courses.__len__(),
            "max_proposals": 2,
            "proposal": proposed_course}

    if form.validate_on_submit():
        proposal = ProposedCourses(prof.id, form.course_name.data, form.speciality.data, form.study_line.data,
                                   form.description.data)
        form.course_name.data = ""
        form.speciality.data = ""
        form.study_line.data = ""
        form.description.data = ""

        pc = db.session.query(ProposedCourses).get(proposal_id)

        pc.course_name = proposal.course_name
        pc.speciality = proposal.speciality
        pc.study_line = proposal.study_line
        pc.description = proposal.description

        db.session.commit()
        return redirect(url_for("professor.view_proposals"))
    return render_template("professor/update_proposal.html", data=data, form=form)


@professor_blueprint.route('/proposals/delete_proposal/')
@professor_blueprint.route('/proposals/delete_proposal/<proposal_id>')
@login_required(2)
def delete_proposal(proposal_id=None):
    if proposal_id is None:
        return redirect(url_for('404'))

    proposed_course = ProposedCourses.query.filter_by(id=proposal_id).first()
    db.session.delete(proposed_course)
    db.session.commit()
    return redirect(url_for("professor.view_proposals"))


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



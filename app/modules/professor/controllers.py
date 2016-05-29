from app import db
from app import login_required
from app.modules.common.models import Course, GradeEvaluation, Student
from app.modules.common.models import Professor, ProposedCourses
from app.modules.professor.forms import ProposalForm
from config import SQLALCHEMY_DATABASE_URI
from flask import Blueprint, render_template, request
from flask import url_for
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

        some_engine = create_engine(SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=some_engine)
        session = Session()
        session.add(proposal)
        session.commit()

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
                grades = list([{"grade": grade.grade, "date": grade.evaluation_date, "id": grade.id} for grade in
                               evaluation.grades])
                final_grade = max(grades, key=lambda x: x["grade"] if x["grade"] else 0)["grade"] if grades else 0
                students.append({"student": student, "contract": contract.id, "group": group.group_number,  "grades": grades, "final_grade": final_grade})
    for student in students:
        students_dict[student["group"]].append(student)
    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "courses": courses,
            "rank_prof": current_proffesor.rank,
            "ranks": ranks,
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

    return url_for('professor.get_students_for_course', course_id=course_id)


def __save_grade(grade_id, value, date):
    if date:
        c_date = datetime.strptime(date, '%d/%m/%Y').date()
        GradeEvaluation.query.filter_by(id=grade_id).update(dict(evaluation_date=c_date))
        db.session.commit()
    if value is not "" and value is None and value is not "absent":
        GradeEvaluation.query.filter_by(id=grade_id).update(dict(grade=int(value)))
        db.session.commit()


def __get_professor_courses(professor) -> [Course]:
    return [professor_role.course for professor_role in professor.professor_roles if professor_role.role_type.id == 1]


def __get_courses_names(courses) -> [str]:
    return [course.course_name for course in courses]


def __get_student_group(student_id) -> int:
    return Student.query.filter_by(id=student_id).first().semigroup.study_group.group_number
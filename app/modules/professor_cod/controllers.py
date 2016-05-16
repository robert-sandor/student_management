from app import login_required, db
from app.modules.common.models import OptionalCourse, Course, Package
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
    optional_courses = OptionalCourse.query.filter_by(active=False).all()
    courses = []
    for optional_course in optional_courses:
        courses.append(optional_course.course)
    data["proposals"] = courses
    data["packages"] = Package.query.all()
    return render_template("professor_cod/proposals.html", data=data)


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

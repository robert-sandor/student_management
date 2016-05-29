from app import login_required, db
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from app.modules.common.models import Professor, ProposedCourses
from app.modules.professor.forms import ProposalForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI

professor = Blueprint('professor', __name__, url_prefix='/prof')


@professor.route('/home/')
@login_required(2)
def home():
    prof = Professor.query.filter_by(id_user=current_user.id).first()

    ranks = {"doctorand": 0,
             "asistent": 1,
             "conferentiar": 2,
             "lector": 3,
             "prof":4}

    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "rank_prof": prof.rank,
            "ranks": ranks}
    return render_template("professor/professor.html", data=data)


@professor.route('/proposals/add_proposal/', methods=['GET', 'POST'])
@login_required(2)
def add_proposal():
    prof = Professor.query.filter_by(id_user=current_user.id).first()
    proposed_courses = ProposedCourses.query.filter_by(professor_id=prof.id).all()
    form = ProposalForm(request.form)
    ranks = {"doctorand": 0,
             "asistent": 1,
             "conferentiar": 2,
             "lector": 3,
             "prof": 4}

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


@professor.route('/proposals/view_proposals/')
@login_required(2)
def view_proposals():
    prof = Professor.query.filter_by(id_user=current_user.id).first()
    proposed_courses = ProposedCourses.query.filter_by(professor_id=prof.id).all()
    data = {"username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "rank_prof": prof.rank,
            "no_proposals": proposed_courses.__len__(),
            "max_proposals": 2,
            "proposals": proposed_courses}
    return render_template("professor/view_proposals.html", data=data)


@professor.route('/proposals/update_proposal/', methods=['GET', 'POST'])
@professor.route('/proposals/update_proposal/<proposal_id>/', methods=['GET', 'POST'])
@login_required(2)
def update_proposal(proposal_id=None):
    if proposal_id is None:
        return redirect(url_for('404'))
    prof = Professor.query.filter_by(id_user=current_user.id).first()
    proposed_courses = ProposedCourses.query.filter_by(professor_id=prof.id).all()
    proposed_course = ProposedCourses.query.filter_by(id=proposal_id).first()
    form = ProposalForm(request.form)
    ranks = {"doctorand": 0,
             "asistent": 1,
             "conferentiar": 2,
             "lector": 3,
             "prof": 4}

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


@professor.route('/proposals/delete_proposal/')
@professor.route('/proposals/delete_proposal/<proposal_id>')
@login_required(2)
def delete_proposal(proposal_id=None):
    if proposal_id is None:
        return redirect(url_for('404'))

    proposed_course = ProposedCourses.query.filter_by(id=proposal_id).first()
    db.session.delete(proposed_course)
    db.session.commit()
    return redirect(url_for("professor.view_proposals"))

from app import login_required
from flask import Blueprint, jsonify, render_template
from flask_login import current_user

professor = Blueprint('professor', __name__, url_prefix='/prof')


@professor.route('/home/')
@login_required(2)
def home():
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email}
    return render_template("professor/professor.html", data=data)
   # return jsonify(data)



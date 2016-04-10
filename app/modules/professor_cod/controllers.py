from app import login_required
from flask import Blueprint, render_template, jsonify
from flask_login import current_user

professor_cod = Blueprint('professor_cod', __name__, url_prefix='/prof_cod')


@professor_cod.route('/home/')
@login_required(3)
def home():
    data = {"username": current_user.username, "role": current_user.role, "email": current_user.email}
    #return render_template("professor_cod/professor_cod.html", data=data)
    return jsonify(data)
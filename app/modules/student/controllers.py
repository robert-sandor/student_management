from app import login_required
from flask import Blueprint, jsonify, render_template
from flask.ext.login import current_user

student = Blueprint('student', __name__, url_prefix='/student')


@student.route('/home/')
@login_required(1)
def home():
    data = {"username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            }
    return render_template('student/welcome.html', data=data)

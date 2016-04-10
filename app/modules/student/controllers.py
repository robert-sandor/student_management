from app import login_required
from flask import Blueprint, jsonify
from flask.ext.login import current_user

student = Blueprint('student', __name__, url_prefix='/student')


@student.route('/home/')
@login_required(1)
def home():
    return jsonify({"username": current_user.username,
                    "e-mail": current_user.email,
                    "role": current_user.role,
                    })

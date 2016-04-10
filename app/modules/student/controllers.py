from app import login_required
from flask import Blueprint

student = Blueprint('student', __name__, url_prefix='/student')


@student.route('/home/')
@login_required(1)
def home():
    return 'Student home'

from flask import Blueprint

student = Blueprint('student', __name__, url_prefix='/student')


@student.route('/home/')
def home():
    return 'Student home'

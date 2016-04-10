from app import login_required
from flask import Blueprint

professor = Blueprint('professor', __name__, url_prefix='/prof')


@professor.route('/home/')
@login_required(2)
def home():
    return 'Professor Home'

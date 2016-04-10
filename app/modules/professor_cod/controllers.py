from app import login_required
from flask import Blueprint

professor_cod = Blueprint('professor_cod', __name__, url_prefix='/prof_cod')


@professor_cod.route('/home/')
@login_required(3)
def home():
    return 'Professor COD Home'

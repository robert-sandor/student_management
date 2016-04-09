from werkzeug.utils import redirect

from flask import Blueprint

base_page = Blueprint('base_page', __name__, url_prefix='/')


@base_page.route('/', methods=['GET'])
def main_page():
    return redirect("/auth/signin", 302)

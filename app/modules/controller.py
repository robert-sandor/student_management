from werkzeug.utils import redirect

from app import app


@app.route('/', methods=['GET'])
def main_page():
    return redirect("/auth/signin", 302)

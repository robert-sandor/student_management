from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(_):
    return render_template('404.html'), 404


from app.modules.mod_auth.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/signin'

@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user


def login_required(role=0):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            urole = current_user.get_role()
            if (urole != role) and (role != 0):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


from app.modules.controller import base_page
from app.modules.admin_staff.controllers import admin_staff
from app.modules.mod_auth.controllers import mod_auth
from app.modules.professor.controllers import professor_blueprint
from app.modules.professor_cod.controllers import professor_cod
from app.modules.student.controllers import student

app.register_blueprint(base_page)
app.register_blueprint(admin_staff)
app.register_blueprint(mod_auth)
app.register_blueprint(professor_blueprint)
app.register_blueprint(professor_cod)
app.register_blueprint(student)

db.create_all()

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(_):
    return render_template('404.html'), 404


from app.modules.controller import base_page
from app.modules.admin_staff.controllers import admin_staff
from app.modules.mod_auth.controllers import mod_auth
from app.modules.professor.controllers import professor
from app.modules.professor_cod.controllers import professor_cod
from app.modules.student.controllers import student

app.register_blueprint(base_page)
app.register_blueprint(admin_staff)
app.register_blueprint(mod_auth)
app.register_blueprint(professor)
app.register_blueprint(professor_cod)
app.register_blueprint(student)

db.create_all()

from app.modules.mod_auth.models import User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

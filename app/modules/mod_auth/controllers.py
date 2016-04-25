from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for
from werkzeug.security import check_password_hash
from flask.ext.login import login_user, login_required, logout_user

from app.modules.mod_auth.forms import LoginForm
from app.modules.mod_auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.username)

            user_routes = {
                1: 'student.home',
                2: 'professor.home',
                3: 'professor_cod.home',
                4: 'admin_staff.home'
            }

            if user.role in range(1, user_routes.__len__() + 1):
                login_user(user)
                return redirect(url_for(user_routes[user.role]))
            else:
                return redirect(url_for('404'))

        flash('Wrong email or password', 'error-message')
    return render_template("auth/signin.html", form=form)


@mod_auth.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")

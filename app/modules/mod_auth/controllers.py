from flask import Blueprint, request, render_template, \
    flash, session, redirect, url_for
from werkzeug.security import check_password_hash
from flask.ext.login import login_user, login_required, logout_user, current_user

from app.modules.mod_auth.forms import LoginForm
from app.modules.mod_auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    user_routes = {
        1: 'student.home',
        2: 'professor.home',
        3: 'professor_cod.home',
        4: 'admin_staff.home'
    }
    
    if request.method == "POST":
        form = LoginForm(request.form)
        
        if form.validate():
            user = User.query.filter_by(email = form.email.data).first()
            
            if user is None:
                flash("No user with email " + form.email.data + " exists !")
                return render_template('auth/signin.html', form=form)
                
            if not check_password_hash(user.password, form.password.data):
                flash("Incorrect email or password !")
                return render_template('auth/signin.html', form=form)
                
            login_user(user, remember = form.remember.data)
            
            return redirect(url_for(user_routes[user.get_role()]))
        
        flash("Incorrect data entered! Try again!")
        return render_template('auth/signin.html', form=form)
    
    else:
        if current_user is not None and current_user.is_authenticated:
            return redirect(url_for(user_routes[current_user.get_role()]))
        
        return render_template('auth/signin.html', form=LoginForm())


@mod_auth.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")

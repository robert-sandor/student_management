from app import db
from app.modules.common.forms import PasswdChangeForm
from app.modules.mod_auth.models import User
from flask import request, render_template, flash
from flask import Blueprint
from flask.ext.login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

mod_common = Blueprint('common', __name__, url_prefix='/common')


@mod_common.route('/passchange/', methods=['GET', 'POST'])
@login_required
def passchange():
    data = {
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

    if request.method == 'POST':

        form = PasswdChangeForm(request.form)

        if form.validate():
            user = User.query.filter_by(id=current_user.get_id()).first()

            if check_password_hash(user.password, form.old_password.data):

                if form.old_password.data == form.new_password.data:
                    flash("New password must be different than the old password!")
                    return render_template('common/settings.html', data=data, form=form)

                if form.new_password.data == form.repeat_password.data:

                    user.password = generate_password_hash(form.new_password.data)
                    db.session.commit()

                    info = "Password updated succesfully"
                    return render_template('common/settings.html', data=data, form=PasswdChangeForm(), info=info)

                else:
                    flash("Repeated password is not the same as the new password!")
                    return render_template('common/settings.html', data=data, form=form)

            else:
                flash("Incorrect password!")
                return render_template('common/settings.html', data=data, form=form)
        else:
            flash("Incorrect data entered!")
            return render_template('common/settings.html', data=data, form=form)

    else:
        # if there is no current user, or he is not authenticated just redirect to 404
        if current_user is None or not current_user.is_authenticated:
            return render_template('404.html')

        return render_template('common/settings.html', data=data, form=PasswdChangeForm())

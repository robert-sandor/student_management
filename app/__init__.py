from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.modules import controller
from app.modules.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)
db.create_all()

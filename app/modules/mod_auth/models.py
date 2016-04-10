from app import db


class User(db.Model):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    #     date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    #     date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    #                               onupdate=db.func.current_timestamp())
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_role(self):
        return self.role

    def __repr__(self):
        return '<User %r>' % self.username

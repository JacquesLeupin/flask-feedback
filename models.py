"""Models for Playlist app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


class User(db.Model):
    """MAKE A of USERS."""

    @classmethod
    def authenticate(cls, username, password):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.String(), nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30),
                    nullable=False)

    last_name = db.Column(db.String(30),
                    nullable=False)

    is_admin = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'{self.username}'

    feedbacks = db.relationship('Feedback', backref="users", cascade="all,delete")

class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.String(), nullable=False)

    username = db.Column(db.String(), db.ForeignKey('users.username'))

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
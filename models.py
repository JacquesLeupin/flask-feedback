"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CHANGEME(db.Model):
    """MAKE A TABLE."""

    __tablename__ = 'CHANGME'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)

    def __repr__(self):
        return f'{self.CHANGEME}'

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
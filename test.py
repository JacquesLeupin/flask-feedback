from app import app
from models import db, connect_db, Cupcake
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///CHANGEME'
db.create_all()
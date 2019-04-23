from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():


    return render_template("index.html")
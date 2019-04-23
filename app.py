from flask import Flask, jsonify, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import NewUserForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():


    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def new_user():

    form = NewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect('/secret')

    else:
        return render_template('register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user():

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=name).first()


        if user.authenticate(name, password):
            session["username"] = user.username
            return redirect('/secret')

        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login_form.html', form=form)

@app.route("/secret")
def secret():

    return "U MADE IT!"
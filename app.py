from flask import Flask, jsonify, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import NewUserForm, LoginForm, EditFeedbackForm, AddFeedbackForm
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def homepage():


    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def new_user():

    form = NewUserForm()

    if session.get("username"):
        user = session["username"]

    if session.get("username"):
        return redirect(f"/users/{user}")

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        
        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect(f'/users/{new_user.username}')

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
            return redirect(f'/users/{name}')

        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login_form.html', form=form)

@app.route("/users/<username>")
def secret(username):

    user = User.query.get_or_404(username)
    feedbacks = user.feedbacks
    if session.get('username'):
        curr_user = session.get('username')
        user = User.query.get_or_404(curr_user)
        user_to_display = User.query.get_or_404(username)

    if (not session.get("username") or session.get('username') != user.username) and not user.is_admin:
        return render_template('401.html'), 401

    if not session.get("username") or session.get('username') != user.username:
        return render_template('401.html'), 401
    else: 
        return render_template('secret.html', name=user_to_display.username, email=user_to_display.email, first_name=user_to_display.first_name, last_name=user_to_display.last_name, feedbacks=feedbacks)

@app.route("/logout")
def logout():

    session.pop('username')
    
    return redirect('/')

@app.route('/feedback/<int:feedback_id>/update', methods=["POST", "GET"])
def feedback_edit(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.users
    username = user.username
    if not session.get("username") or session['username'] != user.username:
        return render_template('401.html'), 401

    form = EditFeedbackForm(obj=feedback)
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template('feedback_form_update.html',
                           form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.users
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{user.username}')


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    user = User.query.get_or_404(username)
    if not session.get("username") or session['username'] != user.username:
        return render_template('401.html'), 401

    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    print('IN ADD FEEDBACK ROUTE')
    user = User.query.get_or_404(username)
    if not session.get("username") or session['username'] != user.username:
        return render_template('401.html'), 401
    
    form = AddFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(username=username, title=title, content=content)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    
    else: 
        return render_template('add_feedback_form.html', form=form, name=username)

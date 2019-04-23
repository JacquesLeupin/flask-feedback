"""Forms for playlist app."""

from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import InputRequired, Email
from flask_wtf import FlaskForm

class NewUserForm(FlaskForm):
    """Form for adding new user."""
    username = StringField("username", validators=[InputRequired()])

    password = PasswordField("password", validators=[InputRequired()])

    email = StringField("email", validators=[InputRequired(), Email()])

    first_name = StringField("first_name", validators=[InputRequired()])

    last_name = StringField("last_name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in."""
    username = StringField("username", validators=[InputRequired()])

    password = PasswordField("password", validators=[InputRequired()])

class EditFeedbackForm(FlaskForm):
    """Form for editing Feedback."""
    title = StringField("title", validators=[InputRequired()])

    content = StringField("content", validators=[InputRequired()])


class AddFeedbackForm(FlaskForm):
    """Form for adding feedback."""
    title = StringField("title", validators=[InputRequired()])

    content = StringField("content", validators=[InputRequired()])
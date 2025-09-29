"""
Forms for Flask Notes app using Flask-WTF.
"""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from flask_babel import lazy_gettext as translate_lazy
from models.database import User

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField(translate_lazy('Username'), validators=[
        DataRequired(message=translate_lazy('Username is required.')),
        Length(min=3, max=80, message=translate_lazy('Username must be between 3 and 80 characters long.'))
    ])
    password = PasswordField(translate_lazy('Password'), validators=[
        DataRequired(message=translate_lazy('Password is required.'))
    ])
    recaptcha = RecaptchaField()
    submit = SubmitField(translate_lazy('Login'))

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField(translate_lazy('Username*'), validators=[
        DataRequired(message=translate_lazy('Username is required.')),
        Length(min=3, max=80, message=translate_lazy('Username must be between 3 and 80 characters long.'))
    ])
    password = PasswordField(translate_lazy('Password*'), validators=[
        DataRequired(message=translate_lazy('Password is required.')),
        Length(min=6, message=translate_lazy('Password must be at least 6 characters long.'))
    ])
    confirm_password = PasswordField(translate_lazy('Confirm Password*'), validators=[
        DataRequired(message=translate_lazy('Please confirm your password.')),
        Length(min=6, message=translate_lazy('Password must be at least 6 characters long.')),
        EqualTo('password', message=translate_lazy('Passwords must match.'))
    ])
    recaptcha = RecaptchaField()
    submit = SubmitField(translate_lazy('Register'))

    def validate_username(self, username):
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).one_or_none()
        if user:
            raise ValidationError(translate_lazy('Username already taken. Please choose another one.'))

class NoteForm(FlaskForm):
    """Form for creating and editing notes."""
    title = StringField(translate_lazy('Title'), validators=[
        DataRequired(message=translate_lazy('Title is required.')),
        Length(min=1, max=200, message=translate_lazy('Title must be between 1 and 200 characters long.'))
    ])
    content = TextAreaField(translate_lazy('Content'), validators=[
        DataRequired(message=translate_lazy('Content is required.')),
        Length(min=1, message=translate_lazy('Content cannot be empty.'))
    ])
    submit = SubmitField(translate_lazy('Save'))


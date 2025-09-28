"""
Forms for Flask Notes app using Flask-WTF.
"""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from models.database import User

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Benutzername', validators=[
        DataRequired(message='Benutzername ist erforderlich.'),
        Length(min=3, max=80, message='Benutzername muss zwischen 3 und 80 Zeichen lang sein.')
    ])
    password = PasswordField('Passwort', validators=[
        DataRequired(message='Passwort ist erforderlich.')
    ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Anmelden')

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Benutzername*', validators=[
        DataRequired(message='Benutzername ist erforderlich.'),
        Length(min=3, max=80, message='Benutzername muss zwischen 3 und 80 Zeichen lang sein.')
    ])
    password = PasswordField('Passwort*', validators=[
        DataRequired(message='Passwort ist erforderlich.'),
        Length(min=6, message='Passwort muss mindestens 6 Zeichen lang sein.')
    ])
    confirm_password = PasswordField('Passwort bestätigen*', validators=[
        DataRequired(message='Bitte bestätigen Sie Ihr Passwort.'),
        Length(min=6, message='Passwort muss mindestens 6 Zeichen lang sein.'),
        EqualTo('password', message='Passwörter müssen übereinstimmen.')
    ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).one_or_none()
        if user:
            raise ValidationError('Benutzername bereits vergeben. Bitte wählen Sie einen anderen.')

class NoteForm(FlaskForm):
    """Form for creating and editing notes."""
    title = StringField('Titel', validators=[
        DataRequired(message='Titel ist erforderlich.'),
        Length(min=1, max=200, message='Titel muss zwischen 1 und 200 Zeichen lang sein.')
    ])
    content = TextAreaField('Inhalt', validators=[
        DataRequired(message='Inhalt ist erforderlich.'),
        Length(min=1, message='Inhalt darf nicht leer sein.')
    ])
    submit = SubmitField('Speichern')


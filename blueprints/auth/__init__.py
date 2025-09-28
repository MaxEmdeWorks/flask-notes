"""
Authentication Blueprint for Flask Notes app.
Handles user login, registration, and logout.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.database import db, User
from models.forms import LoginForm, RegistrationForm

# Create auth blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/", methods=["GET"])
def auth_index():
    """Main auth page - redirects to login."""
    # Redirect authenticated users to notes page
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
    return redirect(url_for('auth.login'))

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Login page and handling."""
    # Redirect authenticated users to notes page
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))

    login_form = LoginForm()
    register_form = RegistrationForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).one_or_none()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash(f"Willkommen zurück, {user.username}!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('notes.index'))
        else:
            flash('Ungültiger Benutzername oder Passwort.', 'error')

    return render_template("auth/auth.html", login_form=login_form, register_form=register_form, tab='login')

@bp.route("/register", methods=["GET", "POST"])
def register():
    """Registration page and handling."""
    # Redirect authenticated users to notes page
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))

    login_form = LoginForm()
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        # Create new user
        user = User(username=register_form.username.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        # User registration successful
        flash('Registrierung erfolgreich! Sie können sich jetzt anmelden.', 'success')
        return redirect(url_for('auth.login'))

    return render_template("auth/auth.html", login_form=login_form, register_form=register_form, tab='register')

@bp.route("/logout")
@login_required
def logout():
    """Logout user."""
    logout_user()
    flash('Sie wurden erfolgreich abgemeldet.', 'info')
    return redirect(url_for('auth.login'))


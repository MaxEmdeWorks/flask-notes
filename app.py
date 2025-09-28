import os

from dotenv import load_dotenv

from flask import Flask, app, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect, generate_csrf

from models.database import db, User
from models import db_utils

import blueprints

def create_app(config=None):
    """Create and configure Flask application instance."""
    # Load environment variables from .env file (only if not in test mode)
    if not config or not config.get('TESTING'):
        load_dotenv()

    app = Flask(__name__)

    # General configuration
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev")   # Load from .env, fallback to "dev"
    app.config['TEMPLATES_AUTO_RELOAD'] = os.getenv("RELOAD_TEMPLATES", False)  # Load from .env, fallback to False

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///notes.db')  # Load from .env, fallback to SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

    # ReCaptcha configuration
    app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

    # Override with provided config (for testing)
    if config:
        app.config.update(config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate
    db_utils.init_app(app)

    # Create tables if using SQLite fallback
    with app.app_context():
        if 'sqlite:///' in app.config['SQLALCHEMY_DATABASE_URI'] and not os.path.exists('instance/notes.db'):
            db.create_all()

    # Initialize CSRF Protection
    CSRFProtect(app)
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    for module in blueprints.submodules:
        app.register_blueprint(module.bp)

    # Default route - redirect to notes if authenticated, otherwise to login
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('notes.index'))
        return redirect(url_for('auth.login'))

    return app

if __name__ == "__main__":
    app = create_app()
    dbg_mode = os.getenv("FLASK_DEBUG", "0")  # Load from .env, fallback to "0"
    app.run(debug=dbg_mode)


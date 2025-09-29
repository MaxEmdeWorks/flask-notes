import os

from dotenv import load_dotenv

from flask import Flask, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_babel import Babel, gettext

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

    # Babel configuration
    app.config['LANGUAGES'] = ['en', 'de']
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

    # Override with provided config (for testing)
    if config:
        app.config.update(config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate
    db_utils.init_app(app)

    # User language preference
    def get_locale():
        """Select the best match for supported languages."""
        # If user is logged in, use their preferred language
        if current_user.is_authenticated and hasattr(current_user, 'get_language'):
            user_lang = current_user.get_language()
            if user_lang and user_lang in app.config['LANGUAGES']:
                return user_lang

        # Check if language is set in session
        if 'language' in session and session['language'] in app.config['LANGUAGES']:
            return session['language']

        # Use browser's preferred language
        return request.accept_languages.best_match(app.config['LANGUAGES']) or app.config['BABEL_DEFAULT_LOCALE']

    # Initialize Babel with locale_selector
    babel = Babel()
    babel.init_app(app, locale_selector=get_locale)

    # Register translation function for templates
    app.jinja_env.globals['translate'] = gettext
    app.jinja_env.globals['_'] = gettext  # Keep backward compatibility

    # Create tables if using SQLite fallback
    with app.app_context():
        if 'sqlite:///' in app.config['SQLALCHEMY_DATABASE_URI'] and not os.path.exists('instance/notes.db'):
            db.create_all()

    # Initialize CSRF Protection
    CSRFProtect(app)

    # Inject configuration variables into templates
    @app.context_processor
    def inject_conf_vars():
        return dict(
            csrf_token=generate_csrf,
            LANGUAGES=app.config['LANGUAGES'],
            CURRENT_LANGUAGE=session.get('language', app.config['BABEL_DEFAULT_LOCALE']),
            get_locale=get_locale
        )

    # Make gettext available in templates
    app.jinja_env.globals.update(_=gettext, translate=gettext)

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

    # Language switching route
    @app.route('/set_language/<language>')
    def set_language(language=None):
        """Set user's preferred language."""
        if language in app.config['LANGUAGES']:
            session['language'] = language
            # If user is logged in, save to database
            if current_user.is_authenticated:
                current_user.set_language(language)
                db.session.commit()
        # Redirect back to referring page or home
        return redirect(request.referrer or url_for('index'))

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


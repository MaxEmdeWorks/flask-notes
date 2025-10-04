# Flask Notes

![CI](https://github.com/MaxEmdeWorks/flask-notes/actions/workflows/ci.yml/badge.svg)

A minimal Flask app that demonstrates auth placeholder, CRUD notes, pagination-ready structure and templates. Uses SQLite (default) or PostgreSQL with Flask-SQLAlchemy and Flask-Migrate for persistent data storage.

**Live demo:** https://flask-notes-0emy.onrender.com/ - first request may take up to a minute while the service spins up

## Quickstart
1. Create venv and install deps
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up environment and database
   ```bash
   # Copy example env file and customize if needed
   cp .env.example .env  # Windows: copy .env.example .env

   # Configure Google reCAPTCHA v2 keys in .env for register/login forms
   # Create keys at https://www.google.com/recaptcha/admin/create
   # For local development, add 'localhost' or '127.0.0.1' to allowed domains
   # Set RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY in .env

   # Configure rate limiting in .env
   # FLASK_LIMITER_ENABLED=True
   # FLASK_LIMITER_DEFAULT_LIMIT="30 per minute"
   # FLASK_LIMITER_STORAGE_URI="memory://"

   # Uses SQLite by default (sqlite:///notes.db)
   # For PostgreSQL: Set DATABASE_URL=postgresql://postgres:dev@localhost:5432/notes

   # Initialize database migrations
   flask db init  # Only needed once
   flask db migrate -m "Initial migration"
   flask db upgrade

   # Optional: Add sample data
   flask seed-db
   ```

3. Run the app
   ```bash
   # Run the app (uses FLASK_APP and FLASK_DEBUG from .env)
   flask run
   # open http://127.0.0.1:5000
   ```

4. Tests and lint
   ```bash
   pytest
   ruff check
   ```

## Features
- ✅ SQLite database (default) with Flask-SQLAlchemy
- ✅ PostgreSQL support (configurable via DATABASE_URL)
- ✅ Database migrations with Flask-Migrate
- ✅ CRUD operations for notes (Create, Read, Update, Delete)
- ✅ Note archiving system (archive/unarchive notes with toggle view)
- ✅ User authentication with Flask-Login (register, login, logout)
- ✅ Google reCAPTCHA v2 integration for security
- ✅ CSRF protection with Flask-WTF
- ✅ User-specific notes (notes are private to each user)
- ✅ Search functionality with pagination
- ✅ Note categories with color-coding and filtering
- ✅ Category management with CRUD operations
- ✅ Responsive Bootstrap UI with modal-based editing
- ✅ Dark/Light theme toggle with system preference detection
- ✅ Modern mobile navigation with offcanvas sidebar
- ✅ Internationalization (i18n) with Flask-Babel (English/German)
- ✅ Rate limiting with Flask-Limiter (configurable, smart timer)
- ✅ Custom rate limit error page with countdown timer
- ✅ Session-based language switching
- ✅ Comprehensive unit tests with pytest
- ✅ Custom CLI commands for database management
- ✅ Bootstrap tooltips

## Rate Limiting

Intelligent rate limiting with Flask-Limiter:
- Smart timer that doesn't reset on page refresh
- Custom error page with countdown
- Configurable via `.env` variables

```bash
FLASK_LIMITER_ENABLED=True
FLASK_LIMITER_DEFAULT_LIMIT="100 per minute"
FLASK_LIMITER_STORAGE_URI="memory://"
```

## Database Commands
```bash
# Create migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations to database
flask db upgrade

# Add sample data with test user (custom command)
flask seed-db

# Create a new user (interactive)
flask create-user
```

## Internationalization (i18n)

Flask-Notes supports multiple languages using Flask-Babel. Currently supported languages:
- English (en) - default
- German (de)

### Managing Translations

Use the provided script to manage translations:

```bash
# Extract, update and compile all translations
python update_translations.py
```

### Adding New Translations

1. Mark strings for translation in your code:
   ```python
   # In Python files (runtime translations, flash messages, etc.)
   from flask_babel import gettext as translate
   flash(translate("Welcome back!"))

   # For forms and class-level definitions (lazy translation)
   from flask_babel import lazy_gettext as translate_lazy
   from wtforms import StringField

   class MyForm(FlaskForm):
       title = StringField(translate_lazy('Title'), validators=[
           DataRequired(message=translate_lazy('Title is required.'))
       ])

   # In Jinja2 templates
   {{ translate("Hello World") }}
   ```

   - Use `translate()` for runtime translations in views, flash messages, and dynamic content.
   - Use `translate_lazy()` for forms, validation messages, and any string that should be translated only when rendered (e.g., WTForms fields).

2. Extract and update translation files:
   ```bash
   python update_translations.py
   ```

3. Edit translation files in `translations/{language}/LC_MESSAGES/messages.po`:
   ```po
   msgid "Hello World"
   msgstr "Hallo Welt"  # Add your translation here
   ```

4. Compile translations and restart server:
   ```bash
   python update_translations.py
   flask run
   ```

## Next steps
- ✅ Add note editing functionality
- ✅ Add pagination and search
- ✅ Add real auth (Flask-Login or JWT) and CSRF-protected forms
- ✅ Add darkmode feature
- ✅ Add multilanguage system
- ✅ Add note archiving system
- ✅ Add rate limiting with smart timer
- ✅ Add note categories for better organization
- Add Redis support for rate limiting in production
- Add admin panel to manage users, view all notes, and display statistics (total users, total notes, and more)
- Add screenshots/GIF to this README


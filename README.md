# Flask Notes

![CI](https://github.com/MaxEmdeWorks/flask-notes/actions/workflows/ci.yml/badge.svg)

A minimal Flask app that demonstrates auth placeholder, CRUD notes, pagination-ready structure and templates. Uses SQLite (default) or PostgreSQL with Flask-SQLAlchemy and Flask-Migrate for persistent data storage.

**Live demo:** https://flask-notes-0emy.onrender.com/ — first request may take up to a minute while the service spins up

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
- ✅ User authentication with Flask-Login (register, login, logout)
- ✅ Google reCAPTCHA v2 integration for security
- ✅ CSRF protection with Flask-WTF
- ✅ User-specific notes (notes are private to each user)
- ✅ Responsive Bootstrap UI with modal-based editing
- ✅ Dark/Light theme toggle with system preference detection
- ✅ Modern mobile navigation with offcanvas sidebar
- ✅ Comprehensive unit tests with pytest
- ✅ Custom CLI commands for database management

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

## Next steps
- ✅ Add note editing functionality
- ✅ Add pagination and search.
- ✅ Add real auth (Flask-Login or JWT) and CSRF-protected forms.
- ✅ Add darkmode feature
- Add admin panel to manage users, view all notes, and display statistics (total users, total notes, and more)
- Add multilanguage system
- Add screenshots/GIF to this README.


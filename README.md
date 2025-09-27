# Flask Notes

![CI](https://github.com/MaxEmdeWorks/flask-notes/actions/workflows/ci.yml/badge.svg)

A minimal Flask app that demonstrates auth placeholder, CRUD notes, pagination-ready structure and templates. Uses SQLite (default) or PostgreSQL with Flask-SQLAlchemy and Flask-Migrate for persistent data storage.

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
- ✅ Responsive Bootstrap UI
- ✅ Comprehensive unit tests with pytest
- ✅ Custom CLI commands for database management

## Database Commands
```bash
# Create migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations to database
flask db upgrade

# Add sample data (custom command)
flask seed-db
```

## Next steps
- ✅ Add note editing functionality
- ✅ Add pagination and search.
- Add real auth (Flask-Login or JWT) and CSRF-protected forms.
- Add darkmode feature
- Add screenshots/GIF to this README.


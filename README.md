# Flask Notes

![CI](https://github.com/MaxEmdeWorks/flask-notes/actions/workflows/ci.yml/badge.svg)

A minimal Flask app that demonstrates auth placeholder, CRUD notes, pagination-ready structure and templates. Uses an in-memory store to keep the scaffold simple.

## Quickstart
1. Create venv and install deps
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up environment and run
   ```bash
   # Copy example env file and customize if needed
   cp .env.example .env  # Windows: copy .env.example .env

   # Run the app (uses FLASK_APP and FLASK_DEBUG from .env)
   flask run
   # open http://127.0.0.1:5000
   ```

3. Tests and lint
   ```bash
   pytest
   ruff check
   ```

## Next steps
- Replace in-memory notes with a real DB (SQLite/PostgreSQL).
- Add pagination and search.
- Add real auth (Flask-Login or JWT) and CSRF-protected forms.
- Add darkmode feature
- Add screenshots/GIF to this README.


import os

from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, abort
from flask_migrate import Migrate

from models.database import db, Note
from models import db_utils

def create_app(config=None):
    """Create and configure Flask application instance."""
    # Load environment variables from .env file (only if not in test mode)
    if not config or not config.get('TESTING'):
        load_dotenv()

    app = Flask(__name__)

    # Configuration
    app.secret_key = os.getenv("SECRET_KEY", "dev")  # Load from .env, fallback to "dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///notes.db')  # Load from .env, fallback to SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

    # Override with provided config (for testing)
    if config:
        app.config.update(config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate
    db_utils.init_app(app)

    # Register routes
    register_routes(app)

    return app

def register_routes(app):
    """Register application routes."""
    # Render the index page with the list of notes
    @app.route("/")
    def index():
        """Render the index page with the list of notes."""
        notes = Note.query.all()
        return render_template("pages/index.html", notes=notes)

    # Add a new note from form data
    @app.route("/add", methods=["POST"])
    def add():
        """Add a new note from form data and redirect back to index."""
        # Get form data
        title = request.form.get("note_title", "").strip()
        content = request.form.get("note_content", "").strip()
        if title and content:
            # Add new note to database
            new_note = Note(title=title, content=content)
            db.session.add(new_note)
            db.session.commit()
        return redirect(url_for("index"))

    # Delete a note by its ID
    @app.route("/delete/<int:note_id>", methods=["POST"])
    def delete(note_id: int):
        """Delete a note by its ID and redirect back to index."""
        # Find and delete note by ID
        note = db.session.get(Note, note_id)
        if not note:
            abort(404)
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for("index"))

if __name__ == "__main__":
    app = create_app()
    dbg_mode = os.getenv("FLASK_DEBUG", "0")  # Load from .env, fallback to "0"
    app.run(debug=dbg_mode)


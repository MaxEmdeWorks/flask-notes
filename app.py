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

    # Create tables if using SQLite fallback
    with app.app_context():
        if 'sqlite:///' in app.config['SQLALCHEMY_DATABASE_URI'] and not os.path.exists('instance/notes.db'):
            db.create_all()

    # Register routes
    register_routes(app)

    return app

def register_routes(app):
    """Register application routes."""
    # Render the index page with the list of notes
    @app.route("/")
    def index():
        """Render the index page with paginated notes."""
        page = request.args.get('page', 1, type=int)
        search_query = request.args.get('search', '').strip()
        per_page = 6

        # Build query with search filter
        query = Note.query
        if search_query:
            query = query.filter(db.or_(Note.title.contains(search_query), Note.content.contains(search_query)))

        # Get paginated notes (using SQLAlchemy's built-in pagination)
        pagination = query.order_by(Note.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

        return render_template("pages/index.html",
            notes=pagination.items,
            current_page=pagination.page,
            total_pages=pagination.pages,
            total_notes=pagination.total,
            search_query=search_query
        )

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

    # Update a note by its ID
    @app.route("/update/<int:note_id>", methods=["POST"])
    def update(note_id: int):
        """Update a note by its ID and redirect back to index."""
        note = db.session.get(Note, note_id)
        if not note:
            abort(404)

        # Get form data
        title = request.form.get("note_title", "").strip()
        content = request.form.get("note_content", "").strip()

        if title and content:
            # Update note fields
            note.title = title
            note.content = content
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


"""
Notes Blueprint for Flask Notes app.
Handles all note-related operations (CRUD).
"""
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from flask_babel import gettext as translate
from models.database import db, Note
from models.forms import NoteForm

# Create notes blueprint
bp = Blueprint('notes', __name__, url_prefix='/notes')

@bp.route("/")
@login_required
def index():
    """Render the index page with paginated notes for current user."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    per_page = 6

    # Build query with search filter for current user's notes only
    query = Note.query.filter_by(user_id=current_user.id)
    if search_query:
        query = query.filter(db.or_(Note.title.contains(search_query), Note.content.contains(search_query)))

    # Get paginated notes (using SQLAlchemy's built-in pagination)
    pagination = query.order_by(Note.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    # Create form for adding new notes
    notes_form = NoteForm()

    return render_template("notes/notes.html",
        notes=pagination.items,
        current_page=pagination.page,
        total_pages=pagination.pages,
        total_notes=pagination.total,
        search_query=search_query,
        notes_form=notes_form
    )

@bp.route("/add", methods=["POST"])
@login_required
def add():
    """Add a new note from form data and redirect back to index."""
    form = NoteForm()

    if form.validate_on_submit():
        # Add new note to database for current user
        new_note = Note(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash(translate('Note successfully created!'), 'success')

    return redirect(url_for("notes.index"))

@bp.route("/update/<int:note_id>", methods=["POST"])
@login_required
def update(note_id: int):
    """Update a note by its ID and redirect back to index."""
    note = db.session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        abort(404)

    form = NoteForm()

    if form.validate_on_submit():
        # Update note fields
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash(translate('Note successfully updated!'), 'success')

    return redirect(url_for("notes.index"))

@bp.route("/edit/<int:note_id>", methods=["GET"])
@login_required
def edit(note_id: int):
    """Get note data for editing modal."""
    note = db.session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        abort(404)

    # Create form with pre-filled data
    form = NoteForm(obj=note)

    return render_template("notes/edit_modal.html", form=form, note=note)

@bp.route("/delete/<int:note_id>", methods=["POST"])
@login_required
def delete(note_id: int):
    """Delete a note by its ID and redirect back to index."""
    # Find and delete note by ID, but only if it belongs to current user
    note = db.session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        abort(404)
    db.session.delete(note)
    db.session.commit()
    flash(translate('Note successfully deleted!'), 'success')
    return redirect(url_for("notes.index"))


"""
Categories Blueprint for Flask Notes app.
Handles all category-related operations (CRUD).
"""
from flask import Blueprint, render_template, redirect, url_for, abort, flash, jsonify, request
from flask_login import login_required, current_user
from flask_babel import gettext as translate
from models.database import db, Category, Note
from models.forms import CategoryForm

# Create categories blueprint
bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route("/")
@login_required
def index():
    """Render the categories management page with pagination and search."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    per_page = 10

    # Build query with search filter for current user's categories only
    query = Category.query.filter_by(user_id=current_user.id)
    if search_query:
        query = query.filter(Category.name.contains(search_query))

    # Get paginated categories (using SQLAlchemy's built-in pagination)
    pagination = query.order_by(Category.name).paginate(page=page, per_page=per_page, error_out=False)

    category_form = CategoryForm()

    # Count notes for each category
    category_counts = {}
    for category in pagination.items:
        category_counts[category.id] = Note.query.filter_by(user_id=current_user.id, category_id=category.id, archived=False).count()

    # Count notes without category
    uncategorized_count = Note.query.filter_by(user_id=current_user.id, category_id=None, archived=False).count()

    return render_template("categories/categories.html",
        categories=pagination.items,
        current_page=pagination.page,
        total_pages=pagination.pages,
        total_categories=pagination.total,
        search_query=search_query,
        category_form=category_form,
        category_counts=category_counts,
        uncategorized_count=uncategorized_count
    )

@bp.route("/add", methods=["POST"])
@login_required
def add():
    """Add a new category."""
    form = CategoryForm()

    if form.validate_on_submit():
        new_category = Category(name=form.name.data, color=form.color.data, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()
        flash(translate('Category successfully created!'), 'success')
    else:
        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for("categories.index"))

@bp.route("/update/<int:category_id>", methods=["POST"])
@login_required
def update(category_id: int):
    """Update a category by its ID."""
    category = db.session.get(Category, category_id)
    if not category or category.user_id != current_user.id:
        abort(404)

    form = CategoryForm(category_id=category_id)

    if form.validate_on_submit():
        category.name = form.name.data
        category.color = form.color.data
        db.session.commit()
        flash(translate('Category successfully updated!'), 'success')
    else:
        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for("categories.index"))

@bp.route("/delete/<int:category_id>", methods=["POST"])
@login_required
def delete(category_id: int):
    """Delete a category by its ID."""
    category = db.session.get(Category, category_id)
    if not category or category.user_id != current_user.id:
        abort(404)

    # Set category_id to None for all notes in this category
    notes = Note.query.filter_by(category_id=category_id, user_id=current_user.id).all()
    for note in notes:
        note.category_id = None

    db.session.delete(category)
    db.session.commit()
    flash(translate('Category successfully deleted! Associated notes are now uncategorized.'), 'success')

    return redirect(url_for("categories.index"))

@bp.route("/get/<int:category_id>", methods=["GET"])
@login_required
def get_category(category_id: int):
    """Get category data for editing (AJAX endpoint)."""
    category = db.session.get(Category, category_id)
    if not category or category.user_id != current_user.id:
        abort(404)

    return jsonify(category.to_dict())


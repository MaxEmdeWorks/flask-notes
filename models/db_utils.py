"""
Database utility script for Flask Notes app.
This script provides commands to manage the database.
"""
import click
from flask.cli import with_appcontext
from models.database import db, Note

@click.command()
@with_appcontext
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo('Initialized the database.')

@click.command()
@with_appcontext
def seed_db():
    """Seed the database with sample data."""
    # Check if there are already notes
    if Note.query.count() > 0:
        click.echo('Database already has notes. Skipping seed.')
        return

    # Add sample notes
    sample_notes = [
        Note(
            title="Note 1",
            content="This is your first note. You can create, read, and delete notes using this app."
        ),
        Note(
            title="Note 2",
            content="Feel free to add more notes and manage them as you like!"
        ),
        Note(
            title="Note 3",
            content="This is a sample note to demonstrate the functionality of the app."
        )
    ]
    for note in sample_notes:
        db.session.add(note)
    db.session.commit()
    click.echo(f'Added {len(sample_notes)} sample notes.')

@click.command()
@with_appcontext
def reset_db():
    """Drop and recreate all tables."""
    db.drop_all()
    db.create_all()
    click.echo('Reset the database.')

# Register commands with the app
def init_app(app):
    """Register database CLI commands with Flask app."""
    app.cli.add_command(init_db)
    app.cli.add_command(seed_db)
    app.cli.add_command(reset_db)


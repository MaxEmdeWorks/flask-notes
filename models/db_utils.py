"""
Database utility script for Flask Notes app.
This script provides commands to manage the database.
"""
import click
from flask.cli import with_appcontext
from models.database import db, Note, User

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
    # Create a test user first if none exists
    test_user = User.query.filter_by(username='testuser').first()
    if not test_user:
        test_user = User(username='testuser')
        test_user.set_password('test123')
        db.session.add(test_user)
        db.session.commit()
        click.echo('Created test user: testuser (password: test123)')

    # Check if there are already notes for this user
    if Note.query.filter_by(user_id=test_user.id).count() > 0:
        click.echo('Test user already has notes. Skipping seed.')
        return

    # Add sample notes for the test user
    sample_notes = [
        Note(
            title="Willkommen bei Flask Notes!",
            content="Dies ist Ihre erste Notiz. Sie können Notizen erstellen, lesen, bearbeiten und löschen.",
            user_id=test_user.id
        ),
        Note(
            title="Funktionen der App",
            content="- Benutzerregistrierung und Anmeldung\n- Persönliche Notizen\n- Suche und Paginierung\n- Responsive Design",
            user_id=test_user.id
        ),
        Note(
            title="Beispiel-Notiz",
            content="Dies ist eine Beispiel-Notiz um die Funktionalität der App zu demonstrieren. Sie können sie bearbeiten oder löschen.",
            user_id=test_user.id
        )
    ]
    for note in sample_notes:
        db.session.add(note)
    db.session.commit()
    click.echo(f'Added {len(sample_notes)} sample notes for test user.')

@click.command()
@with_appcontext
def reset_db():
    """Drop and recreate all tables."""
    db.drop_all()
    db.create_all()
    click.echo('Reset the database.')

@click.command()
@click.option('--username', prompt='Username', help='Username for the new user')
@click.option('--password', prompt='Password', hide_input=True, help='Password for the new user')
@with_appcontext
def create_user(username, password):
    """Create a new user."""
    if User.query.filter_by(username=username).first():
        click.echo(f'User {username} already exists!')
        return

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f'Created user: {username}')

# Register commands with the app
def init_app(app):
    """Register database CLI commands with Flask app."""
    app.cli.add_command(init_db)
    app.cli.add_command(seed_db)
    app.cli.add_command(reset_db)
    app.cli.add_command(create_user)


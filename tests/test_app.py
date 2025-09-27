import sys
import os
import pytest

# Get the parent directory (necessary for imports)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models.database import db, Note

@pytest.fixture
def client():
    """Fixture to create a test client with an in-memory SQLite database."""
    # Create app with test configuration - pass config directly to avoid .env loading
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Force in-memory SQLite for tests
        'WTF_CSRF_ENABLED': False
    }
    app = create_app(config=test_config)

    with app.app_context():
        db.create_all()

        with app.test_client() as test_client:
            yield test_client

        # Clean up after test
        db.session.remove()
        db.drop_all()

# Basic test to check if the index page loads correctly
def test_index(client):
    """Test that the index page loads successfully."""
    resp = client.get("/")
    assert resp.status_code == 200

# Test adding a note
def test_add_note(client):
    """Test that a note can be added successfully."""
    resp = client.post("/add", data={
        "note_title": "Test Note",
        "note_content": "This is a test note"
    })
    assert resp.status_code == 302  # Should redirect

    # Check if note was actually added
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Test Note" in resp.data
    assert b"This is a test note" in resp.data

# Test deleting a note
def test_delete_note(client):
    """Test that a note can be deleted successfully."""
    # First add a note
    note = Note(title="Test Note", content="Test Content")
    db.session.add(note)
    db.session.commit()
    note_id = note.id

    # Delete the note
    resp = client.post(f"/delete/{note_id}")
    assert resp.status_code == 302  # Should redirect

    # Check if note was deleted
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Test Note" not in resp.data


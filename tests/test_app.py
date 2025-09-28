import sys
import os
import pytest

# Get the parent directory (necessary for imports)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models.database import db, Note, User

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

        # Create a test user for authentication
        test_user = User(username='testuser')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()

        with app.test_client() as test_client:
            # Login the test user for all tests
            with test_client.session_transaction() as sess:
                sess['_user_id'] = str(test_user.id)
                sess['_fresh'] = True

            yield test_client

        # Clean up after test
        db.session.remove()
        db.drop_all()

# Basic test to check if the index page loads correctly
def test_index(client):
    """Test that the index page loads successfully."""
    resp = client.get("/notes/")
    assert resp.status_code == 200

# Test adding a note
def test_add_note(client):
    """Test that a note can be added successfully."""
    resp = client.post("/notes/add", data={
        "title": "Test Note",
        "content": "This is a test note"
    })
    assert resp.status_code == 302  # Should redirect

    # Check if note was actually added
    resp = client.get("/notes/")
    assert resp.status_code == 200
    assert b"Test Note" in resp.data
    assert b"This is a test note" in resp.data

# Test deleting a note
def test_delete_note(client):
    """Test that a note can be deleted successfully."""
    # First add a note with user_id (get test user from session)
    with client.session_transaction() as sess:
        user_id = int(sess['_user_id'])

    note = Note(title="Test Note", content="Test Content", user_id=user_id)
    db.session.add(note)
    db.session.commit()
    note_id = note.id

    # Delete the note
    resp = client.post(f"/notes/delete/{note_id}")
    assert resp.status_code == 302  # Should redirect

    # Check if note was deleted
    resp = client.get("/notes/")
    assert resp.status_code == 200
    assert b"Test Note" not in resp.data

# Test that edit modal data is present in index page
def test_edit_modal_in_index(client):
    """Test that the edit modal and necessary data attributes are present."""
    # First add a note with user_id
    with client.session_transaction() as sess:
        user_id = int(sess['_user_id'])

    note = Note(title="Test Title", content="Test Content", user_id=user_id)
    db.session.add(note)
    db.session.commit()

    # Get the index page
    resp = client.get("/notes/")
    assert resp.status_code == 200
    assert b"Test Title" in resp.data
    assert b"Test Content" in resp.data

# Test editing a note - POST update
def test_edit_note_post(client):
    """Test that a note can be updated successfully."""
    # First add a note with user_id
    with client.session_transaction() as sess:
        user_id = int(sess['_user_id'])

    note = Note(title="Original Title", content="Original Content", user_id=user_id)
    db.session.add(note)
    db.session.commit()
    note_id = note.id

    # Update the note
    resp = client.post(f"/notes/update/{note_id}", data={
        "title": "Updated Title",
        "content": "Updated Content"
    })
    assert resp.status_code == 302  # Should redirect

    # Check if note was updated
    resp = client.get("/notes/")
    assert resp.status_code == 200
    assert b"Updated Title" in resp.data
    assert b"Updated Content" in resp.data
    assert b"Original Title" not in resp.data
    assert b"Original Content" not in resp.data

# Test updating non-existent note
def test_update_nonexistent_note(client):
    """Test that updating a non-existent note returns 404."""
    resp = client.post("/notes/update/999", data={
        "title": "Test Title",
        "content": "Test Content"
    })
    assert resp.status_code == 404


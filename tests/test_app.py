import sys
import os

# Get the app from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# Basic test to check if the index page loads correctly
def test_index():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


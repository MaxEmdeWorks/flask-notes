from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")  # Load from .env, fallback to "dev"

# In-memory storage for notes (soon to be replaced with a database)
NOTES = []

# Render the index page with the list of notes
@app.route("/")
def index():
    """
    Render the index page with the list of notes.
    """
    return render_template("pages/index.html", notes=NOTES)

# Add a new note from form data
@app.route("/add", methods=["POST"])
def add():
    """
    Add a new note from form data.
    Redirect back to the index page after adding.
    """
    # Get form data
    title = request.form.get("note_title", "").strip()
    content = request.form.get("note_content", "").strip()
    if title and content:
        # Add new note
        NOTES.append({"id": len(NOTES) + 1, "title": title, "content": content})
    return redirect(url_for("index"))

# Delete a note by its ID
@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id: int):
    """
    Delete a note by its ID.
    Redirect back to the index page after deleting.
    """
    global NOTES
    # Remove note by ID
    NOTES = [n for n in NOTES if n["id"] != note_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    dbg_mode = os.getenv("FLASK_DEBUG", "0") # Load from .env, fallback to "0"
    app.run(debug=dbg_mode)


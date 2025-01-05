from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# Create a Blueprint for view routes
views = Blueprint('views', __name__)


# Route for the home page
@views.route('/', methods=['GET', 'POST'])
@login_required  # Ensure only logged-in users can access this route
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Retrieve the note content from the HTML form
        
        if len(note) < 1:
            flash('Note is too short!', category='error')  # Show error if note is empty or too short
        else:
            # Create a new note associated with the current user
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)  # Add the note to the database session
            db.session.commit()  # Commit the session to save the note
            flash('Note added!', category='success')  # Show success message
    
    return render_template("home.html", user=current_user)  # Render the home page template


# Route to handle note deletion
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # Parse the incoming JSON data from JavaScript
    noteId = note['noteId']  # Extract the note ID from the JSON
    note = Note.query.get(noteId)  # Query the database for the note by ID
    
    if note:
        if note.user_id == current_user.id:  # Ensure the note belongs to the current user
            db.session.delete(note)  # Delete the note from the database session
            db.session.commit()  # Commit the session to apply the deletion
    
    return jsonify({})  # Return an empty JSON response to confirm deletion

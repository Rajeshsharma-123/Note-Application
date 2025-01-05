from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Model for storing user notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each note
    data = db.Column(db.String(10000))  # Content of the note, up to 10,000 characters
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp when the note is created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key linking the note to a user


# Model for storing user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    email = db.Column(db.String(150), unique=True)  # User's email, must be unique
    password = db.Column(db.String(150))  # User's password (hashed)
    first_name = db.Column(db.String(150))  # User's first name
    notes = db.relationship('Note')  # Relationship to link user with their notes

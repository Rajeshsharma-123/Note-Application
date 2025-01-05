from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import the database instance from __init__.py
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__)


# Route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Get email from form input
        password = request.form.get('password')  # Get password from form input
        
        user = User.query.filter_by(email=email).first()  # Check if user exists in the database
        if user:
            if check_password_hash(user.password, password):  # Verify the password
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # Log the user in
                return redirect(url_for('views.home'))  # Redirect to the home page
            else:
                flash('Incorrect password, try again.', category='error')  # Invalid password
        else:
            flash('Email does not exist.', category='error')  # Email not found
    
    return render_template("login.html", user=current_user)  # Render the login page


# Route for user logout
@auth.route('/logout')
@login_required  # Ensure only logged-in users can access this route
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('auth.login'))  # Redirect to the login page


# Route for user sign-up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')  # Get email from form input
        first_name = request.form.get('firstName')  # Get first name from form input
        password1 = request.form.get('password1')  # Get first password entry
        password2 = request.form.get('password2')  # Get second password entry
        
        user = User.query.filter_by(email=email).first()  # Check if email already exists
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new user with hashed password
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)  # Add user to the database
            db.session.commit()  # Commit the transaction
            login_user(new_user, remember=True)  # Log in the newly created user
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))  # Redirect to the home page
    
    return render_template("sign_up.html", user=current_user)  # Render the sign-up page

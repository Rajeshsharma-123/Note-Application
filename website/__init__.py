from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Create a database object for SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # Create the main Flask application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'  # Set the secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Set the database URI
    db.init_app(app)  # Initialize SQLAlchemy with the application

    # Import and register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models
    from .models import User, Note
    
    with app.app_context():
        db.create_all()  # Create all tables

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the login view
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Load user by ID

    return app


# Function to create the database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)  # Create the database
        print('Created Database!')  # Print success message

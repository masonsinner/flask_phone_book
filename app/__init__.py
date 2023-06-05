from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# SQLAlchemy to connect to the database
db = SQLAlchemy(app)

# Migrate that will track DB and App
migrate = Migrate(app, db)

# Make login work
login = LoginManager(app)

# Set up login menu for order
login.login_view = 'login'
login.login_message_category = 'warning'

from app.models import User

# User loader function
@login.user_loader
def load_user(user_id):
    # Implement the logic to load the user object based on the user_id
    # This function should return the user object or None if the user doesn't exist
    return User.query.get(user_id)

# Import the routes after defining the user loader function
from app import routes, models

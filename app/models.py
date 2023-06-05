from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), nullable=False, unique=True)
    username = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    addresses = db.relationship('Address', backref='user', lazy=True)

    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])

    def __repr__(self):
        return f"<User {self.id}\{self.username}>"
    
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_first_name = db.Column(db.String(50), nullable=False)
    ad_last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(75), nullable=False)
    submitter = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Phone Number {self.id}|{self.phone_number}>"

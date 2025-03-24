from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  
    user_type = db.Column(db.String(20), default='member')
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    
    def __init__(self, name, email, contact, password, user_type='member', notes=None):
        self.name = name
        self.email = email
        self.contact = contact
        self.set_password(password)  # Ensure passwords are hashed
        self.user_type = user_type
        self.notes = notes
        

    def __repr__(self):
        return f'<User id:{self.id}, name:{self.name}, email:{self.email}, contact:{self.contact}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


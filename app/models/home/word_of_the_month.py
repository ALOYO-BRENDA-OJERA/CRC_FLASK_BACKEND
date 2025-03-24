from app.extensions import db
from datetime import datetime

class WordOfMonth(db.Model):
    __tablename__ = 'word_of_month'
    
    id = db.Column(db.Integer, primary_key=True)
    banner_image = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
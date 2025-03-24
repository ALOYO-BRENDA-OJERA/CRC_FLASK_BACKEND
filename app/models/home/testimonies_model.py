from datetime import datetime
from app.extensions import db

class Testimony(db.Model):
    __tablename__ = 'testimonies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the person sharing the testimony
    testimony_text = db.Column(db.Text, nullable=False)  # The actual testimony content
    image_url = db.Column(db.String(255), nullable=True)  # Optional field for an image URL
    date_shared = db.Column(db.Date, default=datetime.utcnow, nullable=False)  # Date when the testimony was shared
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    def __init__(self, name, testimony_text, image_url=None, date_shared=None):
        
        self.name = name
        self.testimony_text = testimony_text
        self.image_url = image_url
        self.date_shared = date_shared if date_shared else datetime.utcnow().date()

    def __repr__(self):
        return f"<Testimony {self.id}: {self.name}>"

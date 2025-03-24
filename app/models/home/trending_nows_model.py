from datetime import datetime
from app.extensions import db

class TrendingNow(db.Model):
    __tablename__ = 'trending_nows'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)  # Date for the trending content
    description = db.Column(db.Text, nullable=False)  # Description of the trending item
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    def __init__(self, description, date=None):
        
        self.description = description
        self.date = date if date else datetime.utcnow().date()

    def __repr__(self):
        return f"<TrendingNow {self.id}: {self.description[:50]}...>"

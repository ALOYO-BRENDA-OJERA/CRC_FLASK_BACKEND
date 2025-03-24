from datetime import datetime, date
from app.extensions import db

class DailyDevotion(db.Model):
    __tablename__ = 'daily_devotions'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each devotion
    title = db.Column(db.String(255), nullable=False)  # Title of the devotion
    content = db.Column(db.Text, nullable=False)  # Main content of the devotion
    scripture_reference = db.Column(db.String(255), nullable=True)  # Optional scripture reference for the devotion
    devotion_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)  # Date for the devotion (defaults to today's date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    def __init__(self, title, content, scripture_reference=None, devotion_date=None):
        """
        Initialize a DailyDevotion object.
        :param title: The title of the devotion.
        :param content: The main content of the devotion.
        :param scripture_reference: Optional; reference to a scripture for the devotion.
        :param devotion_date: Optional; the date of the devotion (defaults to today).
        """
        self.title = title
        self.content = content
        self.scripture_reference = scripture_reference
        self.devotion_date = devotion_date if devotion_date else datetime.utcnow().date()

    def __repr__(self):
        return f"<DailyDevotion {self.id}: {self.title} on {self.devotion_date}>"

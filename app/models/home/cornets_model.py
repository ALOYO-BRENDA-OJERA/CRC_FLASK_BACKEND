from datetime import datetime, date
from app.extensions import db

class DailyDevotion(db.Model):
    __tablename__ = 'daily_devotions'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each devotion
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)  # Date for the devotion (defaults to today)
    theme = db.Column(db.String(255), nullable=False)  # Theme of the devotion
    scripture = db.Column(db.String(255), nullable=True)  # Scripture reference for the devotion
    reflection = db.Column(db.Text, nullable=False)  # Reflection content of the devotion
    prayer = db.Column(db.Text, nullable=False)  # Prayer related to the devotion
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    def __init__(self, theme, reflection, prayer, scripture=None, date=None):
        """
        Initialize a DailyDevotion object.
        :param theme: The theme of the devotion.
        :param reflection: The reflection content of the devotion.
        :param prayer: The prayer text for the devotion.
        :param scripture: Optional; reference to a scripture for the devotion.
        :param date: Optional; the date of the devotion (defaults to today).
        """
        self.theme = theme
        self.reflection = reflection
        self.prayer = prayer
        self.scripture = scripture
        self.date = date if date else datetime.utcnow().date()

    def __repr__(self):
        return f"<DailyDevotion {self.id}: {self.theme} on {self.date}>"
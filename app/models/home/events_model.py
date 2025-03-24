from datetime import datetime
from app.extensions import db

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each event
    title = db.Column(db.String(255), nullable=False)  # Title of the event
    description = db.Column(db.Text, nullable=False)  # Description or details about the event
    date = db.Column(db.Date, nullable=False)  # Date of the event
    banner_image = db.Column(db.String(255), nullable=True)  # Image file path or URL
    status = db.Column(db.String(50), nullable=False, default="upcoming")  # Status of the event
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when the event was created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    def __init__(self, title, description, date, banner_image=None, status="upcoming"):
        """
        Initialize an Event object.
        :param title: Title of the event.
        :param description: Description or details about the event.
        :param date: Date when the event will occur.
        :param banner_image: Image filename or URL.
        :param status: Status of the event, defaults to 'upcoming'.
        """
        self.title = title
        self.description = description
        self.date = date
        self.banner_image = banner_image
        self.status = status

    def __repr__(self):
        return f"<Event {self.id}: {self.title} on {self.date}>"


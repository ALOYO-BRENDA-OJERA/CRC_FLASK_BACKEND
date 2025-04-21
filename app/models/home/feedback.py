from datetime import datetime
from app.extensions import db

class Feedback(db.Model):
    __tablename__ = 'Feedback'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each feedback
    email = db.Column(db.String(120), nullable=False)  # Email address of the feedback submitter
    content = db.Column(db.Text, nullable=False)  # Feedback content (e.g., comments or suggestions)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when feedback was submitted
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    def __init__(self, email, content):
        """
        Initialize a Feedback object.
        :param email: Email address of the submitter.
        :param content: The feedback content (text).
        """
        self.email = email
        self.content = content

    def __repr__(self):
        return f"<Feedback {self.id}: {self.content[:50]}... from {self.email}>"

    def to_dict(self):
        """
        Serialize the Feedback object to a dictionary.
        :return: Dictionary containing feedback details.
        """
        return {
            'id': self.id,
            'email': self.email,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
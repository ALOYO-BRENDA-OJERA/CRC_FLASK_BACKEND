from datetime import datetime
from app.extensions import db

class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each subscriber
    email = db.Column(db.String(120), unique=True, nullable=False)  # Subscriber's email address
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when the subscriber was added
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    def __init__(self, email):
        """
        Initialize a Subscriber object.
        :param email: Email address of the subscriber.
        """
        self.email = email

    def __repr__(self):
        return f"<Subscriber {self.id}: {self.email}>"

    def to_dict(self):
        """
        Serialize the Subscriber object to a dictionary.
        :return: Dictionary containing subscriber details.
        """
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
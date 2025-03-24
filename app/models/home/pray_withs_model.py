from datetime import datetime
from app.extensions import db

class PrayWith(db.Model):
    __tablename__ = 'pray_withs'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each prayer request
    name = db.Column(db.String(255), nullable=False)  # Name of the person making the prayer request
    contact = db.Column(db.String(255), nullable=False)  # Contact information (could be phone or email)
    address = db.Column(db.String(255), nullable=True)  # Address of the person (optional)
    prayer_request = db.Column(db.Text, nullable=False)  # Prayer request text
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Date and time the request was submitted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when the request was created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for the last update

    def __init__(self, name, contact, prayer_request, address=None):
        """
        Initialize a PrayWith object.
        :param name: Name of the person submitting the prayer request.
        :param contact: Contact information (phone or email).
        :param prayer_request: The prayer request text.
        :param address: Optional address field.
        """
        self.name = name
        self.contact = contact
        self.prayer_request = prayer_request
        self.address = address

    def __repr__(self):
        return f"<PrayWith {self.id}: {self.name}>"

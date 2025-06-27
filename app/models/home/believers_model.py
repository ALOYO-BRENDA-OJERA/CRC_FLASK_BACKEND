from datetime import datetime
from app.extensions import db

class NewBeliever(db.Model):
    __tablename__ = 'new_believers'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each new believer
    full_name = db.Column(db.String(100), nullable=False)  # Full name of the person
    contact = db.Column(db.String(20), nullable=False)  # Contact number (e.g., phone or WhatsApp)
    email = db.Column(db.String(120), nullable=False)  # Email address
    residence = db.Column(db.String(150), nullable=True)  # Place of residence
    date_saved = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # When they got saved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    def __init__(self, full_name, contact, email, residence=None, date_saved=None):
        """
        Initialize a NewBeliever object.
        :param full_name: Full name of the person.
        :param contact: Contact number (e.g., phone or WhatsApp).
        :param email: Email address.
        :param residence: Optional; place of residence.
        :param date_saved: Optional; date and time they got saved (defaults to now).
        """
        self.full_name = full_name
        self.contact = contact
        self.email = email
        self.residence = residence
        self.date_saved = date_saved if date_saved else datetime.utcnow()

    def __repr__(self):
        return f"<NewBeliever {self.id}: {self.full_name} saved on {self.date_saved.strftime('%Y-%m-%d')}>"

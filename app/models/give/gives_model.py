from datetime import datetime, date
from app.extensions import db

class Give(db.Model):
    __tablename__ = 'give'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the give details
    mobile_money_details = db.Column(db.String(255), nullable=True)  # Mobile money payment details (nullable)
    shillings_account = db.Column(db.String(255), nullable=True)  # Bank account details for shillings payments (nullable)
    dollar_account = db.Column(db.String(255), nullable=True)  # Bank account details for dollar payments (nullable)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the record was created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for when the record was last updated

    def __init__(self, mobile_money_details=None, shillings_account=None, dollar_account=None):
        
        self.mobile_money_details = mobile_money_details
        self.shillings_account = shillings_account
        self.dollar_account = dollar_account

    def __repr__(self):
        return f"<Give {self.id}: Mobile Money: {self.mobile_money_details}, Shillings Account: {self.shillings_account}, Dollar Account: {self.dollar_account}>"

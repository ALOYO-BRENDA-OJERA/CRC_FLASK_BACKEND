from datetime import datetime
from app.extensions import db

class AboutUs(db.Model):
    __tablename__ = 'about_us'

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the about us section
    pastor_image = db.Column(db.String(255), nullable=True)  # Path to the pastor's image (nullable)
    statement_of_faith = db.Column(db.String, nullable=True)  # Statement of faith (nullable)
    ministry_profile = db.Column(db.String, nullable=True)  # Ministry profile (nullable)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the record was created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for when the record was last updated

    def __init__(self, pastor_image=None, statement_of_faith=None, ministry_profile=None):
        
        self.pastor_image = pastor_image
        self.statement_of_faith = statement_of_faith
        self.ministry_profile = ministry_profile

    def __repr__(self):
        return f"<AboutUs {self.id}: Pastor Image: {self.pastor_image}, Statement of Faith: {self.statement_of_faith}, Ministry Profile: {self.ministry_profile}>"

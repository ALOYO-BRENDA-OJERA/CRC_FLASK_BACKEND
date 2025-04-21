from app.extensions import db
from datetime import datetime

class BranchEvent(db.Model):
    __tablename__ = 'branch_events'  # Unique table name to avoid conflicts with existing 'events' table

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    banner_image = db.Column(db.String(255), nullable=True)  # Stores the filename of the uploaded banner
    branch = db.Column(db.String(50), nullable=False, default='main')  # Branch identifier (e.g., mbarara, kampala)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<BranchEvent {self.title} - {self.branch}>"
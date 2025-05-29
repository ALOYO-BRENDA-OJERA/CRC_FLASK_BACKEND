from app.extensions import db
from datetime import datetime

class RhemaBlog(db.Model):
    __tablename__ = 'rhema_blogs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))  # Image file name or path
    date_published = db.Column(db.Date, default=lambda: datetime.utcnow().date())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<RhemaBlog {self.title}>'

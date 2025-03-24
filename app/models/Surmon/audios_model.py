from datetime import datetime, date
from app.extensions import db

class AudioSermon(db.Model):
    __tablename__ = 'audio_sermons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(500), nullable=False)  # Path to the audio file
    thumbnail = db.Column(db.String(500), nullable=True)  # Path to the thumbnail image
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    preacher = db.Column(db.String(255), nullable=False)  # Name of the preacher
    category = db.Column(db.String(100), nullable=True)  # Category of the sermon

    def __repr__(self):
        return f"<AudioSermon {self.title} by {self.preacher}>"

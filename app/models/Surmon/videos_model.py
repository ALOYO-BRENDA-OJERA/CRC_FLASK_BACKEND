from datetime import datetime
from app.extensions import db

class VideoSermon(db.Model):
    __tablename__ = 'video_sermons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(500), nullable=False)  # Path to the video file
    thumbnail_path = db.Column(db.String(500), nullable=True)  # Optional thumbnail for the video
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    preacher = db.Column(db.String(255), nullable=False)  # Name of the preacher

    def __init__(self, title, description, file_path, preacher, thumbnail_path=None):
        
        self.title = title
        self.description = description
        self.file_path = file_path
        self.preacher = preacher
        self.thumbnail_path = thumbnail_path

    def __repr__(self):
        return f"<VideoSermon {self.title} by {self.preacher}>"

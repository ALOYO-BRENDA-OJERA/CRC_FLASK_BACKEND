from datetime import datetime, date
from app.extensions import db



class Ministry(db.Model):
    __tablename__ = 'ministries'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(500), nullable=False)  # Path to the uploaded image
    mission = db.Column(db.Text, nullable=True)
    vision = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, description, image_path, mission=None, vision=None):
        """
        Initialize the Ministry object.
        :param description: The ministry's description.
        :param image_path: Path to the uploaded image.
        :param mission: Mission statement of the ministry (optional).
        :param vision: Vision statement of the ministry (optional).
        """
        self.description = description
        self.image_path = image_path
        self.mission = mission
        self.vision = vision

    def __repr__(self):
        return f"<Ministry {self.id}>"

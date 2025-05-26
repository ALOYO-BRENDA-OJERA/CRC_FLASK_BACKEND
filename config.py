# from flask import Flask
# from app.extensions import db
# from config import Config  # Import your Config class

# def create_app():
#     app = Flask(__name__)

#     # Load configuration
#     app.config.from_object(Config)  # Load your config class

#     # Initialize extensions
#     db.init_app(app)

#     return app

class Config:
    """Flask application configuration."""
    SECRET_KEY = 'your_secret_key'  # Match app/__init__.py
    DEBUG = True  # Set to False in production
    CORS_ORIGINS = "http://localhost:3000"  # For CORS
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://aimugorg_CRC-ADMIN:Jera$2025!Brenda@localhost:3306/aimugorg_CRC_SYSTEM'
    
  # MySQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # For Flask-JWT-Extended

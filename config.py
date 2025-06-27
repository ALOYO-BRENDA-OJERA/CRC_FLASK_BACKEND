class Config:
    """Flask application configuration."""
    SECRET_KEY = 'your_secret_key'  # Match app/__init__.py
    DEBUG = True  # Set to False in production
    CORS_ORIGINS = "http://localhost:3000"  # For CORS

    # Updated for Render PostgreSQL DB
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = "mysql+pymysql://aimugorg_DATABASE_ADMIN:AIM-crc2025@localhost/aimugorg_CRC_SYSTEM"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # For Flask-JWT-Extended
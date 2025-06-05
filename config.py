class Config:
    """Flask application configuration."""
    SECRET_KEY = 'your_secret_key'  # Match app/__init__.py
    DEBUG = True  # Set to False in production
    CORS_ORIGINS = "http://localhost:3000"  # For CORS

    # Updated for Render PostgreSQL DB
    SQLALCHEMY_DATABASE_URI = 'postgresql://crc_system_user:7qf5LUDILR9VD2528SYi77vWkEfBjjoK@dpg-d10pedi4d50c73b1v1l0-a.oregon-postgres.render.com/crc_system'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # For Flask-JWT-Extended
class Config:
    """Flask application configuration."""
    SECRET_KEY = 'your_secret_key'  # Match app/__init__.py
    DEBUG = True  # Set to False in production
    CORS_ORIGINS = "http://localhost:3000"  # For CORS

    # Updated for Crane Cloud DB
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://twhgdmijufqepffu:PwW%3Cj%2BZdCEAPhny8SGppbPhEVWK5MQ%3CV@102.134.147.233:32764/nydmvxboekldqtghkqsbkybh'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # For Flask-JWT-Extended

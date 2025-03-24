from flask import Flask
from app.extensions import db
from config import Config  # Import your Config class

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)  # Load your config class

    # Initialize extensions
    db.init_app(app)

    return app

from flask import Flask
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)  # Initialize Flask app
    app.config.from_object(Config)

    # Enable CORS for React frontend (localhost:3000) with all methods and headers
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

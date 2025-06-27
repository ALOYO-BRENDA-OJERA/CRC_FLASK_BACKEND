from app import create_app
from config import Config

# Create the app instance
app = create_app()

if __name__ == "__main__":
    # Run the app with debug mode from Config
    app.run(debug=Config.DEBUG)
    
    
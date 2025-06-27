import sys
import os

# Point to your virtual environment's python executable
sys.executable = "/home/aimugorg/BACKEND/venv/bin/python3"

# Add your project directory to sys.path
sys.path.insert(0, "/home/aimugorg/BACKEND")

# Activate your virtual environment
activate_this = "/home/aimugorg/BACKEND/venv/bin/activate_this.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import create_app

application = create_app()

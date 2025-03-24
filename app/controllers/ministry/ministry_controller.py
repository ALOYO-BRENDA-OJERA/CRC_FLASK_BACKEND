from flask import Blueprint, request, jsonify
from app.models.ministry.ministries_model import Ministry
from app.extensions import db
from werkzeug.utils import secure_filename
import os

# Create Blueprint for Ministry routes
ministries_bp = Blueprint('ministries', __name__, url_prefix='/api/v1/ministries')

# Define the upload folder (Update this path based on your project structure)
UPLOAD_FOLDER = 'C:\\Users\\aloyo\\Downloads\\images'  # Adjust this path as needed
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}  # Allowed image file extensions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

# Create a new ministry
@ministries_bp.route('/create_ministry', methods=['POST'])
def create_ministry():
    try:
        data = request.form
        image_file = request.files.get('image')

        # Validate the input
        if 'description' not in data:
            return jsonify({"message": "Description is required"}), 400
        if not image_file or not allowed_file(image_file.filename):
            return jsonify({"message": "Invalid image file format or no image uploaded"}), 400

        # Save the image file
        image_filename = secure_filename(image_file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_path)

        # Create the ministry entry in the database
        ministry = Ministry(
            description=data['description'],
            image_path=image_path,
            mission=data.get('mission'),
            vision=data.get('vision')
        )

        db.session.add(ministry)
        db.session.commit()

        return jsonify({"message": "Ministry created successfully", "ministry_id": ministry.id}), 201

    except Exception as e:
        db.session.rollback()  # Ensure that the session is rolled back in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get a ministry by id
@ministries_bp.route('/ministries/<int:id>', methods=['GET'])
def get_ministry(id):
    try:
        ministry = Ministry.query.get(id)
        if ministry:
            return jsonify({
                "id": ministry.id,
                "description": ministry.description,
                "image_path": ministry.image_path,
                "mission": ministry.mission,
                "vision": ministry.vision,
                "created_at": ministry.created_at,
                "updated_at": ministry.updated_at
            })
        else:
            return jsonify({"message": "Ministry not found"}), 404
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update a ministry by id
@ministries_bp.route('/ministries/<int:id>', methods=['PUT'])
def update_ministry(id):
    try:
        data = request.form
        ministry = Ministry.query.get(id)

        if not ministry:
            return jsonify({"message": "Ministry not found"}), 404

        # Update fields
        ministry.description = data.get('description', ministry.description)
        ministry.mission = data.get('mission', ministry.mission)
        ministry.vision = data.get('vision', ministry.vision)

        # Handle image file upload if a new image is provided
        image_file = request.files.get('image')
        if image_file and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image_file.save(image_path)
            ministry.image_path = image_path

        db.session.commit()

        return jsonify({"message": "Ministry updated successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete a ministry by id
@ministries_bp.route('/ministries/<int:id>', methods=['DELETE'])
def delete_ministry(id):
    try:
        ministry = Ministry.query.get(id)
        if not ministry:
            return jsonify({"message": "Ministry not found"}), 404

        # Optionally, delete the image file from the server
        if os.path.exists(ministry.image_path):
            os.remove(ministry.image_path)

        db.session.delete(ministry)
        db.session.commit()

        return jsonify({"message": "Ministry deleted successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

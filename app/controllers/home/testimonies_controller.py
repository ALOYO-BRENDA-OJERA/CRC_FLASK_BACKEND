from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from app.models.home.testimonies_model import Testimony
from app.extensions import db

# Create Blueprint for Testimony routes
testimony_bp = Blueprint('testimony', __name__, url_prefix='/api/v1/testimonies')

UPLOAD_FOLDER = r'C:\rhema\testimonies'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@testimony_bp.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Create a new testimony
@testimony_bp.route('/testimony', methods=['POST'])
def create_testimony():
    try:
        # Check if it's a form submission with file or a JSON request
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with file upload
            name = request.form.get('name')
            testimony_text = request.form.get('testimony_text')
            date_shared = request.form.get('date_shared')
            
            if not name or not testimony_text:
                return jsonify({"message": "Name and testimony text are required"}), 400
            
            # Handle image upload if present
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    image_filename = filename
            
            # Create a new Testimony instance
            testimony = Testimony(
                name=name,
                testimony_text=testimony_text,
                image_url=image_filename,  # Store just the filename
                date_shared=date_shared  # Optional; defaults to today's date
            )
        else:
            # Handle JSON data without file
            data = request.get_json()
            
            # Create a new Testimony instance
            testimony = Testimony(
                name=data.get('name'),
                testimony_text=data.get('testimony_text'),
                image_url=data.get('image_url'),  # This would be a URL, not a file
                date_shared=data.get('date_shared')  # Optional; defaults to today's date
            )

        # Add to the session and commit to save it
        db.session.add(testimony)
        db.session.commit()

        return jsonify({
            "message": "Testimony created successfully", 
            "id": testimony.id,
            "image_url": testimony.image_url
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get all testimonies
@testimony_bp.route('/testimonies', methods=['GET'])
def get_testimonies():
    try:
        testimonies = Testimony.query.all()

        if testimonies:
            result = []
            for testimony in testimonies:
                # Return just the filename, like in word_of_month
                result.append({
                    "id": testimony.id,
                    "name": testimony.name,
                    "testimony_text": testimony.testimony_text,
                    "image_url": testimony.image_url,  # Just return the filename
                    "date_shared": testimony.date_shared,
                    "created_at": testimony.created_at,
                    "updated_at": testimony.updated_at
                })

            return jsonify(result)

        return jsonify([])  # Return empty array instead of 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get a specific testimony by ID
@testimony_bp.route('/testimony/<int:id>', methods=['GET'])
def get_testimony(id):
    try:
        testimony = Testimony.query.get(id)

        if testimony:
            # Return just the filename, like in word_of_month
            return jsonify({
                "id": testimony.id,
                "name": testimony.name,
                "testimony_text": testimony.testimony_text,
                "image_url": testimony.image_url,  # Just return the filename
                "date_shared": testimony.date_shared,
                "created_at": testimony.created_at,
                "updated_at": testimony.updated_at
            })

        return jsonify({"message": "Testimony not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update a testimony by ID
@testimony_bp.route('/testimony/<int:id>', methods=['PUT'])
def update_testimony(id):
    try:
        testimony = Testimony.query.get(id)

        if not testimony:
            return jsonify({"message": "Testimony not found"}), 404

        # Check if it's a form submission with file or a JSON request
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with possible file upload
            if 'name' in request.form:
                testimony.name = request.form.get('name')
            if 'testimony_text' in request.form:
                testimony.testimony_text = request.form.get('testimony_text')
            if 'date_shared' in request.form:
                testimony.date_shared = request.form.get('date_shared')
            
            # Handle image upload if present
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    # Delete old image if it exists
                    if testimony.image_url and os.path.exists(os.path.join(UPLOAD_FOLDER, testimony.image_url)):
                        os.remove(os.path.join(UPLOAD_FOLDER, testimony.image_url))
                    
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    testimony.image_url = filename
        else:
            # Handle JSON data without file
            data = request.get_json()
            
            # Update fields with provided data
            testimony.name = data.get('name', testimony.name)
            testimony.testimony_text = data.get('testimony_text', testimony.testimony_text)
            testimony.image_url = data.get('image_url', testimony.image_url)
            testimony.date_shared = data.get('date_shared', testimony.date_shared)

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Testimony updated successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete a testimony by ID
@testimony_bp.route('/testimony/<int:id>', methods=['DELETE'])
def delete_testimony(id):
    try:
        testimony = Testimony.query.get(id)

        if not testimony:
            return jsonify({"message": "Testimony not found"}), 404

        # Delete the image file if it exists
        if testimony.image_url:
            file_path = os.path.join(UPLOAD_FOLDER, testimony.image_url)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Delete the testimony
        db.session.delete(testimony)
        db.session.commit()

        return jsonify({"message": "Testimony deleted successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500
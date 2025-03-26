from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from app.models.home.word_of_the_month import WordOfMonth
from app.extensions import db

# Blueprint setup
word_of_month_bp = Blueprint('word_of_month', __name__, url_prefix='/api/v1/word-of-month')

# Configuration
UPLOAD_FOLDER = r'C:\rhema'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve image files
@word_of_month_bp.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    """Serve a banner image from the upload folder."""
    return send_from_directory(UPLOAD_FOLDER, filename)

# Create a new Word of the Month entry
@word_of_month_bp.route('/create_word', methods=['POST'])
def create_word_of_month():
    """Create a new Word of the Month with a title and banner image."""
    try:
        # Validate banner file presence
        if 'banner' not in request.files:
            return jsonify({"message": "No banner file provided"}), 400
        
        file = request.files['banner']
        title = request.form.get('title')
        
        # Validate title
        if not title:
            return jsonify({"message": "Title is required"}), 400
        
        # Validate and save file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Create new WordOfMonth instance
            word = WordOfMonth(
                banner_image=filename,
                title=title
            )
            
            db.session.add(word)
            db.session.commit()
            
            return jsonify({
                "message": "Word of Month created successfully",
                "data": {
                    "id": word.id,
                    "banner_image": word.banner_image,
                    "title": word.title,
                    "created_at": word.created_at
                }
            }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get all Word of the Month entries
@word_of_month_bp.route('/get_all_word', methods=['GET'])
def get_word_of_month():
    """Retrieve all Word of the Month entries, ordered by creation date."""
    try:
        words = WordOfMonth.query.order_by(WordOfMonth.created_at.desc()).all()
        return jsonify([{
            "id": word.id,
            "banner_image": word.banner_image,
            "title": word.title,
            "created_at": word.created_at
        } for word in words]), 200
        
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get a single Word of the Month entry by ID
@word_of_month_bp.route('/get/<int:id>', methods=['GET'])
def get_single_word_of_month(id):
    """Retrieve a single Word of the Month entry by its ID."""
    try:
        word = WordOfMonth.query.get(id)
        if word:
            return jsonify({
                "data": {
                    "id": word.id,
                    "banner_image": word.banner_image,
                    "title": word.title,
                    "created_at": word.created_at
                }
            }), 200
        return jsonify({"message": "Word of Month not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update an existing Word of the Month entry
@word_of_month_bp.route('/<int:id>', methods=['PUT'])
def update_word_of_month(id):
    """Update an existing Word of the Month entry by ID."""
    try:
        word = WordOfMonth.query.get(id)
        if not word:
            return jsonify({"message": "Word of Month not found"}), 404

        # Get form data
        title = request.form.get('title')
        if not title:
            return jsonify({"message": "Title is required"}), 400

        # Update title
        word.title = title

        # Update banner if provided
        if 'banner' in request.files:
            file = request.files['banner']
            if file and allowed_file(file.filename):
                # Delete old file
                old_file_path = os.path.join(UPLOAD_FOLDER, word.banner_image)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                
                # Save new file
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                word.banner_image = filename

        db.session.commit()
        
        return jsonify({
            "message": "Word of Month updated successfully",
            "data": {
                "id": word.id,
                "banner_image": word.banner_image,
                "title": word.title,
                "created_at": word.created_at
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a Word of the Month entry
@word_of_month_bp.route('/<int:id>', methods=['DELETE'])
def delete_word_of_month(id):
    """Delete a Word of the Month entry by ID and remove its banner image."""
    try:
        word = WordOfMonth.query.get(id)
        if word:
            file_path = os.path.join(UPLOAD_FOLDER, word.banner_image)
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.delete(word)
            db.session.commit()
            return jsonify({"message": "Word of Month deleted successfully"}), 200
        return jsonify({"message": "Word of Month not found"}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
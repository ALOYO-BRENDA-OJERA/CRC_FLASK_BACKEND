from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from app.models.home.word_of_the_month import WordOfMonth
from app.extensions import db

word_of_month_bp = Blueprint('word_of_month', __name__, url_prefix='/api/v1/word-of-month')

UPLOAD_FOLDER = r'C:\rhema'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@word_of_month_bp.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@word_of_month_bp.route('/create_word', methods=['POST'])
def create_word_of_month():
    try:
        if 'banner' not in request.files:
            return jsonify({"message": "No banner file provided"}), 400
            
        file = request.files['banner']
        title = request.form.get('title')
        
        if not title:
            return jsonify({"message": "Title is required"}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            word = WordOfMonth(
                banner_image=filename,  # Store just the filename, not the full path
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

@word_of_month_bp.route('/get_all_word', methods=['GET'])
def get_word_of_month():
    try:
        words = WordOfMonth.query.order_by(WordOfMonth.created_at.desc()).all()
        return jsonify([{
            "id": word.id,
            "banner_image": word.banner_image,
            "title": word.title,
            "created_at": word.created_at
        } for word in words])
        
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@word_of_month_bp.route('/<int:id>', methods=['DELETE'])
def delete_word_of_month(id):
    try:
        word = WordOfMonth.query.get(id)
        if word:
            # Update this to handle just the filename, not the full path
            file_path = os.path.join(UPLOAD_FOLDER, word.banner_image)
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.delete(word)
            db.session.commit()
            return jsonify({"message": "Word of Month deleted successfully"})
        return jsonify({"message": "Word of Month not found"}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
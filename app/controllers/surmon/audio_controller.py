from flask import Blueprint, request, jsonify, send_file, send_from_directory
from app.models.Surmon.audios_model import AudioSermon
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime


# Create Blueprint for Audio Sermon routes
audio_sermons_bp = Blueprint('audio_sermons', __name__, url_prefix='/api/v1/audio_sermons')


# Define the upload folders
AUDIO_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads', 'audio_sermons')
THUMBNAIL_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads', 'thumbnails')

# Create directories if they don't exist
os.makedirs(AUDIO_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_UPLOAD_FOLDER, exist_ok=True)


ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'flac', 'ogg'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_audio_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS


def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


# Serve thumbnail images
@audio_sermons_bp.route('/thumbnails/<filename>', methods=['GET'])
def serve_thumbnail(filename):
    return send_from_directory(THUMBNAIL_UPLOAD_FOLDER, filename)


# Create a new audio sermon
@audio_sermons_bp.route('/create_audio_sermons', methods=['POST'])
def create_audio_sermon():
    try:
        data = request.form
        audio_file = request.files.get('file')
        thumbnail_file = request.files.get('thumbnail')

        # Validate the input
        if 'title' not in data or 'preacher' not in data:
            return jsonify({"message": "Missing required fields"}), 400
        if not audio_file or not allowed_audio_file(audio_file.filename):
            return jsonify({"message": "Invalid audio file or no file uploaded"}), 400

        # Process audio file
        audio_filename = secure_filename(audio_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        audio_filename = f"{timestamp}_{audio_filename}"
        audio_file.save(os.path.join(AUDIO_UPLOAD_FOLDER, audio_filename))

        # Process thumbnail if provided
        thumbnail_filename = None
        if thumbnail_file and allowed_image_file(thumbnail_file.filename):
            thumbnail_filename = secure_filename(thumbnail_file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            thumbnail_filename = f"{timestamp}_{thumbnail_filename}"
            thumbnail_file.save(os.path.join(THUMBNAIL_UPLOAD_FOLDER, thumbnail_filename))

        # Create the audio sermon entry in the database
        audio_sermon = AudioSermon(
            title=data['title'],
            description=data.get('description', ''),
            file_path=os.path.join(AUDIO_UPLOAD_FOLDER, audio_filename),
            thumbnail=thumbnail_filename,  # Store just the filename
            preacher=data['preacher'],
            category=data.get('category', '')
        )
        
        db.session.add(audio_sermon)
        db.session.commit()

        # Prepare response with full URL for thumbnail if it exists
        thumbnail_url = None
        if thumbnail_filename:
            thumbnail_url = f"/api/v1/audio_sermons/thumbnails/{thumbnail_filename}"

        return jsonify({
            "message": "Audio sermon created successfully", 
            "sermon_id": audio_sermon.id,
            "sermon": {
                "id": audio_sermon.id,
                "title": audio_sermon.title,
                "description": audio_sermon.description,
                "preacher": audio_sermon.preacher,
                "category": audio_sermon.category,
                "thumbnail": thumbnail_url,
                "uploaded_at": audio_sermon.uploaded_at.isoformat() if audio_sermon.uploaded_at else None
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


# Get all audio sermons
@audio_sermons_bp.route('/list_sermons', methods=['GET'])
def list_sermons():
    try:
        sermons = AudioSermon.query.all()
        return jsonify([{
            "id": sermon.id,
            "title": sermon.title,
            "description": sermon.description,
            "preacher": sermon.preacher,
            "category": sermon.category,
            "thumbnail": f"/api/v1/audio_sermons/thumbnails/{sermon.thumbnail}" if sermon.thumbnail else None,
            "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None
        } for sermon in sermons])
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


# Get an audio sermon by id
@audio_sermons_bp.route('/get_audio_sermons/<int:id>', methods=['GET'])
def get_audio_sermon(id):
    try:
        sermon = AudioSermon.query.get(id)
        if sermon:
            return jsonify({
                "id": sermon.id,
                "title": sermon.title,
                "description": sermon.description,
                "file_path": sermon.file_path,
                "thumbnail": f"/api/v1/audio_sermons/thumbnails/{sermon.thumbnail}" if sermon.thumbnail else None,
                "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None,
                "preacher": sermon.preacher,
                "category": sermon.category
            })
        else:
            return jsonify({"message": "Audio sermon not found"}), 404
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


# Stream an audio file
@audio_sermons_bp.route('/stream_audio/<int:id>', methods=['GET'])
def stream_audio(id):
    try:
        sermon = AudioSermon.query.get(id)
        if sermon and os.path.exists(sermon.file_path):
            return send_file(sermon.file_path, as_attachment=False)
        else:
            return jsonify({"message": "Audio sermon not found or file missing"}), 404
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


# Update an audio sermon by id
@audio_sermons_bp.route('/update_audio_sermons/<int:id>', methods=['PUT'])
def update_audio_sermon(id):
    try:
        data = request.form
        sermon = AudioSermon.query.get(id)

        if not sermon:
            return jsonify({"message": "Audio sermon not found"}), 404

        # Update fields
        sermon.title = data.get('title', sermon.title)
        sermon.description = data.get('description', sermon.description)
        sermon.preacher = data.get('preacher', sermon.preacher)
        sermon.category = data.get('category', sermon.category)

        # Handle file upload if a new file is provided
        audio_file = request.files.get('file')
        if audio_file and allowed_audio_file(audio_file.filename):
            # Delete the old file if it exists
            if os.path.exists(sermon.file_path):
                try:
                    os.remove(sermon.file_path)
                except Exception as e:
                    print(f"Error deleting old file: {e}")
            
            # Save new file
            audio_filename = secure_filename(audio_file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            audio_filename = f"{timestamp}_{audio_filename}"
            audio_file.save(os.path.join(AUDIO_UPLOAD_FOLDER, audio_filename))
            sermon.file_path = os.path.join(AUDIO_UPLOAD_FOLDER, audio_filename)

        # Handle thumbnail upload if a new thumbnail is provided
        thumbnail_file = request.files.get('thumbnail')
        if thumbnail_file and allowed_image_file(thumbnail_file.filename):
            # Delete the old thumbnail if it exists
            if sermon.thumbnail:
                old_thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, sermon.thumbnail)
                if os.path.exists(old_thumbnail_path):
                    try:
                        os.remove(old_thumbnail_path)
                    except Exception as e:
                        print(f"Error deleting old thumbnail: {e}")
            
            # Save new thumbnail
            thumbnail_filename = secure_filename(thumbnail_file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            thumbnail_filename = f"{timestamp}_{thumbnail_filename}"
            thumbnail_file.save(os.path.join(THUMBNAIL_UPLOAD_FOLDER, thumbnail_filename))
            sermon.thumbnail = thumbnail_filename

        db.session.commit()

        # Prepare response with full URL for thumbnail if it exists
        thumbnail_url = None
        if sermon.thumbnail:
            thumbnail_url = f"/api/v1/audio_sermons/thumbnails/{sermon.thumbnail}"

        return jsonify({
            "message": "Audio sermon updated successfully",
            "sermon": {
                "id": sermon.id,
                "title": sermon.title,
                "description": sermon.description,
                "preacher": sermon.preacher,
                "category": sermon.category,
                "thumbnail": thumbnail_url,
                "uploaded_at": sermon.uploaded_at.isoformat() if sermon.uploaded_at else None
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


# Delete an audio sermon by id
@audio_sermons_bp.route('/delete_audio_sermons/<int:id>', methods=['DELETE'])
def delete_audio_sermon(id):
    try:
        sermon = AudioSermon.query.get(id)
        if not sermon:
            return jsonify({"message": "Audio sermon not found"}), 404

        # Delete the file from the server
        if os.path.exists(sermon.file_path):
            try:
                os.remove(sermon.file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")

        # Delete the thumbnail if it exists
        if sermon.thumbnail:
            thumbnail_path = os.path.join(THUMBNAIL_UPLOAD_FOLDER, sermon.thumbnail)
            if os.path.exists(thumbnail_path):
                try:
                    os.remove(thumbnail_path)
                except Exception as e:
                    print(f"Error deleting thumbnail: {e}")

        db.session.delete(sermon)
        db.session.commit()

        return jsonify({"message": "Audio sermon deleted successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

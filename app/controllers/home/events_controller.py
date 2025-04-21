from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.models.home.events_model import Event
from app.extensions import db

# Blueprint definition
event_bp = Blueprint('event', __name__, url_prefix='/api/v1/events')

# Use the same upload folder as word_of_month
UPLOAD_FOLDER = r'C:\rhema'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@event_bp.route('/images/<filename>', methods=['GET'])
def serve_event_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@event_bp.route('/create_event', methods=['POST'])
def create_event():
    try:
        if 'banner' not in request.files:
            return jsonify({"message": "No banner file provided"}), 400
            
        file = request.files['banner']
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        
        if not title or not description or not date_str:
            return jsonify({"message": "Title, description, and date are required"}), 400
        
        # Parse date string to date object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            event = Event(
                title=title,
                description=description,
                date=date,
                banner_image=filename
            )
            
            db.session.add(event)
            db.session.commit()
            
            return jsonify({
                "message": "Event created successfully",
                "data": {
                    "id": event.id,
                    "banner_image": event.banner_image,
                    "title": event.title,
                    "description": event.description,
                    "date": str(event.date),
                    "created_at": event.created_at
                }
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@event_bp.route('/get_all_events', methods=['GET'])
def get_all_events():
    try:
        events = Event.query.order_by(Event.created_at.desc()).all()
        return jsonify([{
            "id": event.id,
            "banner_image": event.banner_image,
            "title": event.title,
            "description": event.description,
            "date": str(event.date),
            "created_at": str(event.created_at)
        } for event in events])
        
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@event_bp.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    try:
        event = Event.query.get(id)
        if event:
            # Handle just the filename, not the full path
            if event.banner_image:
                file_path = os.path.join(UPLOAD_FOLDER, event.banner_image)
                if os.path.exists(file_path):
                    os.remove(file_path)
            db.session.delete(event)
            db.session.commit()
            return jsonify({"message": "Event deleted successfully"})
        return jsonify({"message": "Event not found"}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@event_bp.route('/<int:id>', methods=['PUT'])
def update_event(id):
    try:
        event = Event.query.get(id)
        if not event:
            return jsonify({"message": "Event not found"}), 404
            
        # Update text fields
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        
        if title:
            event.title = title
        if description:
            event.description = description
        if date_str:
            try:
                event.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
            
        # Handle banner image update if provided
        if 'banner' in request.files:
            file = request.files['banner']
            if file and allowed_file(file.filename):
                # Delete old image if it exists
                if event.banner_image:
                    old_file_path = os.path.join(UPLOAD_FOLDER, event.banner_image)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # Save new image
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                event.banner_image = filename
        
        db.session.commit()
        
        return jsonify({
            "message": "Event updated successfully",
            "data": {
                "id": event.id,
                "banner_image": event.banner_image,
                "title": event.title,
                "description": event.description,
                "date": str(event.date),
                "created_at": str(event.created_at)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500







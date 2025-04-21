from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.models.About.branch_event import BranchEvent
from app.extensions import db

# Blueprint definition with a unique name
branch_event_bp = Blueprint('branch_event', __name__, url_prefix='/api/v1/branch-events')

# Upload folder configuration
UPLOAD_FOLDER = r'C:\rhema'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
VALID_BRANCHES = ['main', 'mbarara', 'kampala', 'jinja', 'soroti', 'china', 'kireka', 'wakiso', 'gulu', 'tororo']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@branch_event_bp.route('/images/<path:filename>', methods=['GET'], endpoint='serve_branch_image')
def serve_branch_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@branch_event_bp.route('/add-branch-event', methods=['POST'], endpoint='add_branch_event')
def add_branch_event():
    try:
        if 'banner' not in request.files:
            return jsonify({"message": "No banner file provided"}), 400

        file = request.files['banner']
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        branch = request.form.get('branch', 'main').lower()  # Normalize to lowercase

        if not title or not description or not date_str:
            return jsonify({"message": "Title, description, and date are required"}), 400

        if branch not in VALID_BRANCHES:
            return jsonify({"message": f"Invalid branch. Must be one of {VALID_BRANCHES}"}), 400

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, branch, filename)
            os.makedirs(os.path.join(UPLOAD_FOLDER, branch), exist_ok=True)
            file.save(filepath)

            event = BranchEvent(
                title=title,
                description=description,
                date=date,
                banner_image=f"{branch}/{filename}",
                branch=branch
            )

            db.session.add(event)
            db.session.commit()

            return jsonify({
                "message": "Branch event added successfully",
                "data": {
                    "id": event.id,
                    "banner_image": event.banner_image,
                    "title": event.title,
                    "description": event.description,
                    "date": str(event.date),
                    "branch": event.branch,
                    "created_at": str(event.created_at),
                    "updated_at": str(event.updated_at)
                }
            }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@branch_event_bp.route('/list-branch-events', methods=['GET'], endpoint='list_branch_events')
def list_branch_events():
    try:
        branch = request.args.get('branch', '').lower()  # Normalize to lowercase
        query = BranchEvent.query.order_by(BranchEvent.created_at.desc())

        if branch:
            if branch not in VALID_BRANCHES:
                return jsonify({"message": f"Invalid branch. Must be one of {VALID_BRANCHES}"}), 400
            query = query.filter_by(branch=branch)

        events = query.all()
        return jsonify([{
            "id": event.id,
            "banner_image": event.banner_image,
            "title": event.title,
            "description": event.description,
            "date": str(event.date),
            "branch": event.branch,
            "created_at": str(event.created_at),
            "updated_at": str(event.updated_at)
        } for event in events])

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@branch_event_bp.route('/manage-branch-event/<int:id>', methods=['DELETE'], endpoint='remove_branch_event')
def remove_branch_event(id):
    try:
        event = BranchEvent.query.get(id)
        if event:
            if event.banner_image:
                file_path = os.path.join(UPLOAD_FOLDER, event.banner_image)
                if os.path.exists(file_path):
                    os.remove(file_path)
            db.session.delete(event)
            db.session.commit()
            return jsonify({"message": "Branch event removed successfully"})
        return jsonify({"message": "Branch event not found"}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@branch_event_bp.route('/manage-branch-event/<int:id>', methods=['PUT'], endpoint='modify_branch_event')
def modify_branch_event(id):
    try:
        event = BranchEvent.query.get(id)
        if not event:
            return jsonify({"message": "Branch event not found"}), 404

        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        branch = request.form.get('branch', '').lower()  # Normalize to lowercase

        if title:
            event.title = title
        if description:
            event.description = description
        if date_str:
            try:
                event.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
        if branch:
            if branch not in VALID_BRANCHES:
                return jsonify({"message": f"Invalid branch. Must be one of {VALID_BRANCHES}"}), 400
            event.branch = branch

        if 'banner' in request.files:
            file = request.files['banner']
            if file and allowed_file(file.filename):
                if event.banner_image:
                    old_file_path = os.path.join(UPLOAD_FOLDER, event.banner_image)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, branch or event.branch, filename)
                os.makedirs(os.path.join(UPLOAD_FOLDER, branch or event.branch), exist_ok=True)
                file.save(filepath)
                event.banner_image = f"{branch or event.branch}/{filename}"

        db.session.commit()

        return jsonify({
            "message": "Branch event modified successfully",
            "data": {
                "id": event.id,
                "banner_image": event.banner_image,
                "title": event.title,
                "description": event.description,
                "date": str(event.date),
                "branch": event.branch,
                "created_at": str(event.created_at),
                "updated_at": str(event.updated_at)
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
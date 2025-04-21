from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.home.feedback import Feedback
from app.extensions import db

feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/v1/feedback')

@feedback_bp.route('/submit', methods=['POST'])
def submit_feedback():
    """
    Submit feedback (open to all users).
    Expects JSON payload with 'email' and 'content'.
    """
    try:
        data = request.get_json()
        email = data.get('email')
        content = data.get('content')

        if not email:
            return jsonify({"message": "Email is required"}), 400
        if not content:
            return jsonify({"message": "Feedback content is required"}), 400
        if '@' not in email or '.' not in email:
            return jsonify({"message": "Invalid email format"}), 400

        new_feedback = Feedback(email=email, content=content)
        db.session.add(new_feedback)
        db.session.commit()

        return jsonify({"message": "Feedback submitted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@feedback_bp.route('/list', methods=['GET'])
@jwt_required()
def list_feedback():
    """
    Retrieve all feedback entries (admin only).
    Returns a list of feedback objects.
    """
    try:
        current_user = get_jwt_identity()
        if current_user['user_type'] != 'admin':
            return jsonify({"message": "Unauthorized: Admin access required"}), 403

        feedback = Feedback.query.all()
        return jsonify({
            "message": "Feedback retrieved successfully",
            "feedback": [f.to_dict() for f in feedback]
        }), 200
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@feedback_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_feedback(id):
    """
    Retrieve a single feedback entry by ID (admin only).
    """
    try:
        current_user = get_jwt_identity()
        if current_user['user_type'] != 'admin':
            return jsonify({"message": "Unauthorized: Admin access required"}), 403

        feedback = Feedback.query.get_or_404(id)
        return jsonify({
            "message": "Feedback retrieved successfully",
            "feedback": feedback.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@feedback_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_feedback(id):
    """
    Delete a feedback entry by ID (admin only).
    """
    try:
        current_user = get_jwt_identity()
        if current_user['user_type'] != 'admin':
            return jsonify({"message": "Unauthorized: Admin access required"}), 403

        feedback = Feedback.query.get_or_404(id)
        db.session.delete(feedback)
        db.session.commit()

        return jsonify({"message": "Feedback deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500
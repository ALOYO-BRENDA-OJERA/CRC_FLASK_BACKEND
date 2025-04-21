from flask import Blueprint, request, jsonify
from app.models.users.subscribers import Subscriber
from app.extensions import db

# Create Blueprint for Subscriber routes
subscribers_bp = Blueprint('subscribers', __name__, url_prefix='/api/v1/subscriber')

# Subscribe to newsletter
@subscribers_bp.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"message": "Email is required"}), 400

        # Validate email format (basic check)
        if '@' not in email or '.' not in email:
            return jsonify({"message": "Invalid email format"}), 400

        # Check if email is already subscribed
        existing_subscriber = Subscriber.query.filter_by(email=email).first()
        if existing_subscriber:
            return jsonify({"message": "Email is already subscribed"}), 400

        # Create a new subscriber
        new_subscriber = Subscriber(email=email)
        db.session.add(new_subscriber)
        db.session.commit()

        return jsonify({"message": "Successfully subscribed to the newsletter"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500
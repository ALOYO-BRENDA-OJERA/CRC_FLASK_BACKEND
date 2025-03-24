from flask import Blueprint, request, jsonify
from app.models.home.pray_withs_model import PrayWith
from app.extensions import db

# Create Blueprint for PrayWith routes
pray_with_bp = Blueprint('pray_with', __name__, url_prefix='/api/v1/prayer_request')

# Create a new prayer request
@pray_with_bp.route('/create', methods=['POST'])
def create_prayer_request():
    try:
        data = request.get_json()

        # Create a new PrayWith instance
        prayer_request = PrayWith(
            name=data.get('name'),
            contact=data.get('contact'),
            prayer_request=data.get('prayer_request'),
            address=data.get('address')  # Optional address
        )

        # Add to the session and commit to save it
        db.session.add(prayer_request)
        db.session.commit()

        return jsonify({"message": "Prayer request submitted successfully", "id": prayer_request.id}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get all prayer requests
@pray_with_bp.route('/get_all', methods=['GET'])
def get_prayer_requests():
    try:
        prayer_requests = PrayWith.query.all()

        if prayer_requests:
            result = []
            for prayer_request in prayer_requests:
                result.append({
                    "id": prayer_request.id,
                    "name": prayer_request.name,
                    "contact": prayer_request.contact,
                    "address": prayer_request.address,
                    "prayer_request": prayer_request.prayer_request,
                    "date_submitted": prayer_request.date_submitted,
                    "created_at": prayer_request.created_at,
                    "updated_at": prayer_request.updated_at
                })

            return jsonify(result)

        return jsonify({"message": "No prayer requests found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get a specific prayer request by ID
@pray_with_bp.route('/pray_with/<int:id>', methods=['GET'])
def get_prayer_request(id):
    try:
        prayer_request = PrayWith.query.get(id)

        if prayer_request:
            return jsonify({
                "id": prayer_request.id,
                "name": prayer_request.name,
                "contact": prayer_request.contact,
                "address": prayer_request.address,
                "prayer_request": prayer_request.prayer_request,
                "date_submitted": prayer_request.date_submitted,
                "created_at": prayer_request.created_at,
                "updated_at": prayer_request.updated_at
            })

        return jsonify({"message": "Prayer request not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update a prayer request by ID
@pray_with_bp.route('/pray_with/<int:id>', methods=['PUT'])
def update_prayer_request(id):
    try:
        prayer_request = PrayWith.query.get(id)

        if not prayer_request:
            return jsonify({"message": "Prayer request not found"}), 404

        # Get data from request
        data = request.get_json()

        # Update fields with provided data
        prayer_request.name = data.get('name', prayer_request.name)
        prayer_request.contact = data.get('contact', prayer_request.contact)
        prayer_request.prayer_request = data.get('prayer_request', prayer_request.prayer_request)
        prayer_request.address = data.get('address', prayer_request.address)

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Prayer request updated successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete a prayer request by ID
@pray_with_bp.route('/pray_with/<int:id>', methods=['DELETE'])
def delete_prayer_request(id):
    try:
        prayer_request = PrayWith.query.get(id)

        if not prayer_request:
            return jsonify({"message": "Prayer request not found"}), 404

        # Delete the prayer request
        db.session.delete(prayer_request)
        db.session.commit()

        return jsonify({"message": "Prayer request deleted successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

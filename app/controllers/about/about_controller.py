from flask import Blueprint, request, jsonify
from app.models.About.about_us_model import AboutUs
from app.extensions import db

# Create Blueprint for AboutUs routes
about_us_bp = Blueprint('about_us', __name__, url_prefix='/api/v1/about')

# Create or update an About Us record
@about_us_bp.route('/create_about_us', methods=['POST', 'PUT'])
def create_or_update_about_us():
    try:
        data = request.get_json()

        # Check if AboutUs record already exists (in this case, assuming a single record for 'About Us')
        about_us = AboutUs.query.first()

        # If not exist, create new record
        if not about_us:
            about_us = AboutUs(
                pastor_image=data.get('pastor_image'),
                statement_of_faith=data.get('statement_of_faith'),
                ministry_profile=data.get('ministry_profile')
            )
            db.session.add(about_us)
            db.session.commit()
            return jsonify({"message": "About Us record created successfully", "id": about_us.id}), 201

        # Update existing record
        about_us.pastor_image = data.get('pastor_image', about_us.pastor_image)
        about_us.statement_of_faith = data.get('statement_of_faith', about_us.statement_of_faith)
        about_us.ministry_profile = data.get('ministry_profile', about_us.ministry_profile)

        db.session.commit()
        return jsonify({"message": "About Us record updated successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get About Us record
@about_us_bp.route('/get_about_us', methods=['GET'])
def get_about_us():
    try:
        about_us = AboutUs.query.first()

        if about_us:
            return jsonify({
                "id": about_us.id,
                "pastor_image": about_us.pastor_image,
                "statement_of_faith": about_us.statement_of_faith,
                "ministry_profile": about_us.ministry_profile,
                "created_at": about_us.created_at,
                "updated_at": about_us.updated_at
            })
        else:
            return jsonify({"message": "About Us record not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete About Us record
@about_us_bp.route('/delete_about_us', methods=['DELETE'])
def delete_about_us():
    try:
        about_us = AboutUs.query.first()

        if not about_us:
            return jsonify({"message": "About Us record not found"}), 404

        # Delete the record
        db.session.delete(about_us)
        db.session.commit()

        return jsonify({"message": "About Us record deleted successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

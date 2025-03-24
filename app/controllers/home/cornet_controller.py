from flask import Blueprint, request, jsonify
from app.models.home.cornets_model import DailyDevotion
from app.extensions import db

# Create Blueprint for DailyDevotion routes
daily_devotion_bp = Blueprint('daily_devotion', __name__, url_prefix='/api/v1/devotion')

# Create a new Daily Devotion
@daily_devotion_bp.route('/daily_devotion', methods=['POST'])
def create_daily_devotion():
    try:
        data = request.get_json()

        # Create a new DailyDevotion instance
        daily_devotion = DailyDevotion(
            title=data.get('title'),
            content=data.get('content'),
            scripture_reference=data.get('scripture_reference'),
            devotion_date=data.get('devotion_date')
        )

        # Add to the session and commit to save it
        db.session.add(daily_devotion)
        db.session.commit()

        return jsonify({"message": "Daily Devotion created successfully", "id": daily_devotion.id}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get a list of Daily Devotions
@daily_devotion_bp.route('/daily_devotions', methods=['GET'])
def get_daily_devotions():
    try:
        daily_devotions = DailyDevotion.query.all()

        if daily_devotions:
            result = []
            for devotion in daily_devotions:
                result.append({
                    "id": devotion.id,
                    "title": devotion.title,
                    "content": devotion.content,
                    "scripture_reference": devotion.scripture_reference,
                    "devotion_date": devotion.devotion_date,
                    "created_at": devotion.created_at,
                    "updated_at": devotion.updated_at
                })

            return jsonify(result)

        return jsonify({"message": "No devotions found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get a specific Daily Devotion by ID
@daily_devotion_bp.route('/daily_devotion/<int:id>', methods=['GET'])
def get_daily_devotion(id):
    try:
        daily_devotion = DailyDevotion.query.get(id)

        if daily_devotion:
            return jsonify({
                "id": daily_devotion.id,
                "title": daily_devotion.title,
                "content": daily_devotion.content,
                "scripture_reference": daily_devotion.scripture_reference,
                "devotion_date": daily_devotion.devotion_date,
                "created_at": daily_devotion.created_at,
                "updated_at": daily_devotion.updated_at
            })

        return jsonify({"message": "Daily Devotion not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update a Daily Devotion by ID
@daily_devotion_bp.route('/daily_devotion/<int:id>', methods=['PUT'])
def update_daily_devotion(id):
    try:
        daily_devotion = DailyDevotion.query.get(id)

        if not daily_devotion:
            return jsonify({"message": "Daily Devotion not found"}), 404

        # Get data from request
        data = request.get_json()

        # Update fields with provided data
        daily_devotion.title = data.get('title', daily_devotion.title)
        daily_devotion.content = data.get('content', daily_devotion.content)
        daily_devotion.scripture_reference = data.get('scripture_reference', daily_devotion.scripture_reference)
        daily_devotion.devotion_date = data.get('devotion_date', daily_devotion.devotion_date)

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Daily Devotion updated successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete a Daily Devotion by ID
@daily_devotion_bp.route('/daily_devotion/<int:id>', methods=['DELETE'])
def delete_daily_devotion(id):
    try:
        daily_devotion = DailyDevotion.query.get(id)

        if not daily_devotion:
            return jsonify({"message": "Daily Devotion not found"}), 404

        # Delete the devotion
        db.session.delete(daily_devotion)
        db.session.commit()

        return jsonify({"message": "Daily Devotion deleted successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

from flask import Blueprint, request, jsonify
from app.models.home.cornets_model import DailyDevotion
from app.extensions import db
from datetime import datetime

# Create Blueprint for DailyDevotion routes
daily_devotion_bp = Blueprint('daily_devotion', __name__, url_prefix='/api/v1/devotion')

# Create one or more Daily Devotions
@daily_devotion_bp.route('/daily_devotion', methods=['POST'])
def create_daily_devotion():
    try:
        data = request.get_json()

        # Check if data is a list (for bulk creation) or a single dict
        if isinstance(data, list):
            created_ids = []
            for devotion_data in data:
                # Validate required fields
                if not all(key in devotion_data for key in ['theme', 'reflection', 'prayer']):
                    return jsonify({"message": "Missing required fields (theme, reflection, prayer)"}), 400
                
                # Parse date if provided, otherwise use default from model
                date_str = devotion_data.get('date')
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()

                # Create a new DailyDevotion instance
                daily_devotion = DailyDevotion(
                    theme=devotion_data.get('theme'),
                    reflection=devotion_data.get('reflection'),
                    prayer=devotion_data.get('prayer'),
                    scripture=devotion_data.get('scripture'),  # Optional
                    date=date_obj
                )
                db.session.add(daily_devotion)
                created_ids.append(daily_devotion.id)  # Store ID before commit

            # Commit all devotions in one transaction
            db.session.commit()
            return jsonify({"message": "Daily Devotions created successfully", "ids": created_ids}), 201

        # Handle single devotion (backward compatibility)
        elif isinstance(data, dict):
            if not all(key in data for key in ['theme', 'reflection', 'prayer']):
                return jsonify({"message": "Missing required fields (theme, reflection, prayer)"}), 400
            
            date_str = data.get('date')
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()

            daily_devotion = DailyDevotion(
                theme=data.get('theme'),
                reflection=data.get('reflection'),
                prayer=data.get('prayer'),
                scripture=data.get('scripture'),
                date=date_obj
            )
            db.session.add(daily_devotion)
            db.session.commit()
            return jsonify({"message": "Daily Devotion created successfully", "id": daily_devotion.id}), 201

        else:
            return jsonify({"message": "Invalid data format; expected object or array"}), 400

    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": "Invalid date format; use YYYY-MM-DD", "error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
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
                    "date": str(devotion.date),  # Convert date to string for JSON
                    "theme": devotion.theme,
                    "scripture": devotion.scripture,
                    "reflection": devotion.reflection,
                    "prayer": devotion.prayer,
                    "created_at": str(devotion.created_at),
                    "updated_at": str(devotion.updated_at)
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
                "date": str(daily_devotion.date),
                "theme": daily_devotion.theme,
                "scripture": daily_devotion.scripture,
                "reflection": daily_devotion.reflection,
                "prayer": daily_devotion.prayer,
                "created_at": str(daily_devotion.created_at),
                "updated_at": str(daily_devotion.updated_at)
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
        daily_devotion.theme = data.get('theme', daily_devotion.theme)
        daily_devotion.reflection = data.get('reflection', daily_devotion.reflection)
        daily_devotion.prayer = data.get('prayer', daily_devotion.prayer)
        daily_devotion.scripture = data.get('scripture', daily_devotion.scripture)
        if data.get('date'):
            daily_devotion.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Daily Devotion updated successfully"})

    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": "Invalid date format; use YYYY-MM-DD", "error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
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
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500
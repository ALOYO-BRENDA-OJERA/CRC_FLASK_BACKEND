from flask import Blueprint, request, jsonify
from app.models.give.gives_model import Give
from app.extensions import db

# Create Blueprint for Give routes
give_bp = Blueprint('give', __name__, url_prefix='/api/v1/give')

# Create a new give record
@give_bp.route('/create_give', methods=['POST'])
def create_give():
    try:
        data = request.get_json()

        # Extract details from request
        mobile_money_details = data.get('mobile_money_details')
        shillings_account = data.get('shillings_account')
        dollar_account = data.get('dollar_account')

        # Create a new Give record
        give = Give(
            mobile_money_details=mobile_money_details,
            shillings_account=shillings_account,
            dollar_account=dollar_account
        )

        # Add to the database
        db.session.add(give)
        db.session.commit()

        return jsonify({"message": "Give record created successfully", "give_id": give.id}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get a give record by id
@give_bp.route('/get_give/<int:id>', methods=['GET'])
def get_give(id):
    try:
        give = Give.query.get(id)

        if give:
            return jsonify({
                "id": give.id,
                "mobile_money_details": give.mobile_money_details,
                "shillings_account": give.shillings_account,
                "dollar_account": give.dollar_account,
                "created_at": give.created_at,
                "updated_at": give.updated_at
            })
        else:
            return jsonify({"message": "Give record not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update a give record by id
@give_bp.route('/update_give/<int:id>', methods=['PUT'])
def update_give(id):
    try:
        data = request.get_json()
        give = Give.query.get(id)

        if not give:
            return jsonify({"message": "Give record not found"}), 404

        # Update the record with new data
        give.mobile_money_details = data.get('mobile_money_details', give.mobile_money_details)
        give.shillings_account = data.get('shillings_account', give.shillings_account)
        give.dollar_account = data.get('dollar_account', give.dollar_account)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Give record updated successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete a give record by id
@give_bp.route('/delete_give/<int:id>', methods=['DELETE'])
def delete_give(id):
    try:
        give = Give.query.get(id)

        if not give:
            return jsonify({"message": "Give record not found"}), 404

        # Delete the record
        db.session.delete(give)
        db.session.commit()

        return jsonify({"message": "Give record deleted successfully"})

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

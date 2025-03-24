from flask import Blueprint, request, jsonify
from app.models.users.users_model import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Create Blueprint for User routes
users_bp = Blueprint('users', __name__, url_prefix='/api/v1/user' )

# Create a new user
@users_bp.route('/create_users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        # Check if required fields are present
        if not all(field in data for field in ('name', 'email', 'contact', 'password')):
            return jsonify({"message": "Missing required fields"}), 400

        # Ensure user does not already exist
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"message": "User with this email already exists"}), 400

        # Create a new user
        new_user = User(
            name=data['name'],
            email=data['email'],
            contact=data['contact'],
            password=data['password']  # Password will be hashed inside the model
        )
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "user": new_user.id}), 201

    except Exception as e:
        db.session.rollback()  # Ensure that the session is rolled back in case of error
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get user details by id
@users_bp.route('/get_users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        if user:
            return jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "contact": user.contact,
                "user_type": user.user_type,
                "notes": user.notes
            })
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update user information
@users_bp.route('/update_users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()

        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Update fields (we assume fields like name, email, contact, etc. can be updated)
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'contact' in data:
            user.contact = data['contact']
        if 'password' in data:
            user.set_password(data['password'])
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'notes' in data:
            user.notes = data['notes']

        db.session.commit()

        return jsonify({"message": "User updated successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Delete a user
@users_bp.route('/delete_users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

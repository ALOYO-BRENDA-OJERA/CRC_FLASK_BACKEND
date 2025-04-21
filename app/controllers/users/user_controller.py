from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models.users.users_model import User
from app.models.users.subscribers import Subscriber
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

# Create Blueprint for User routes
users_bp = Blueprint('users', __name__, url_prefix='/api/v1/user')

# Initialize JWTManager (configured in main app)
jwt = JWTManager()

# Blacklist for revoked tokens (in-memory for simplicity; use Redis in production)
blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist

# Create a new user (Registration)
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
            password=data['password'],  # Password will be hashed inside the model
            user_type=data.get('user_type', 'user')  # Default to 'user'
        )
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Login and issue JWT
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Invalid credentials"}), 401

        # Create JWT with user info
        identity = {'id': user.id, 'email': user.email, 'user_type': user.user_type}
        access_token = create_access_token(identity=identity, expires_delta=timedelta(hours=1))

        # Set JWT in HTTP-only cookie
        response = make_response(jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "user_type": user.user_type
            }
        }))
        response.set_cookie(
            'access_token',
            access_token,
            httponly=True,
            secure=True,  # Set to False for local development without HTTPS
            samesite='Strict',
            max_age=3600  # 1 hour
        )
        return response, 200

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Logout and revoke JWT
@users_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']
        blacklist.add(jti)  # Add token to blacklist
        response = make_response(jsonify({"message": "Logged out successfully"}))
        response.set_cookie('access_token', '', expires=0, httponly=True, secure=True, samesite='Strict')
        return response, 200
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Protected dashboard endpoint
@users_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    try:
        current_user = get_jwt_identity()
        if current_user['user_type'] != 'admin':
            return jsonify({"message": "Unauthorized: Admin access required"}), 403
        return jsonify({
            "message": "Welcome to the admin dashboard",
            "user": current_user
        }), 200
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Get user details by id
@users_bp.route('/get_users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        current_user = get_jwt_identity()
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        if current_user['user_type'] != 'admin' and current_user['id'] != id:
            return jsonify({"message": "Unauthorized: Cannot access other users' data"}), 403
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "contact": user.contact,
            "user_type": user.user_type,
            "notes": user.notes
        })
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# Update user information
@users_bp.route('/update_users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    try:
        current_user = get_jwt_identity()
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        if current_user['user_type'] != 'admin' and current_user['id'] != id:
            return jsonify({"message": "Unauthorized: Cannot update other users' data"}), 403

        data = request.get_json()
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'contact' in data:
            user.contact = data['contact']
        if 'password' in data:
            user.set_password(data['password'])
        if 'user_type' in data and current_user['user_type'] == 'admin':
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
@jwt_required()
def delete_user(id):
    try:
        current_user = get_jwt_identity()
        if current_user['user_type'] != 'admin':
            return jsonify({"message": "Unauthorized: Admin access required"}), 403

        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500


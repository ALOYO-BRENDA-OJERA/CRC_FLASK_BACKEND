from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models.users.users_model import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import traceback
from sqlalchemy.exc import SQLAlchemyError

# Create Blueprint for User routes
users_bp = Blueprint('users', __name__, url_prefix='/api/v1/user')




@users_bp.route('/login', methods=['POST'])
def login():
    try:
        # Parse JSON data
        data = request.get_json()
        if not data:
            print("No JSON data provided in request")
            return jsonify({"message": "Invalid request: JSON data required"}), 400

        email = data.get('email', '').strip()
        password = data.get('password', '')

        # Validate input
        if not email or not password:
            print(f"Missing required fields: email={email}, password={'[provided]' if password else '[missing]'}")
            return jsonify({"message": "Email and password are required"}), 400

        if '@' not in email:
            print(f"Invalid email format: {email}")
            return jsonify({"message": "Invalid email format"}), 400

        # Query user
        print(f"Querying user with email: {email}")
        user = User.query.filter_by(email=email).first()

        if not user:
            print(f"No user found with email: {email}")
            return jsonify({"message": "Invalid email or password"}), 401

        # Check password
        print(f"Checking password for user: {email}")
        print(f"Stored hash: {user.password[:30]}...")  # Log partial hash for security
        if not check_password_hash(user.password, password):
            print("Password verification failed")
            return jsonify({"message": "Invalid email or password"}), 401

        # Check user type
        if user.user_type != 'admin':
            print(f"User {email} is not an admin, user_type: {user.user_type}")
            return jsonify({"message": "Admin access required"}), 403

        # Create JWT with 20-minute expiration
        print(f"Generating JWT for user: {email}")
        identity = {'id': user.id, 'email': user.email, 'user_type': user.user_type}
        try:
            access_token = create_access_token(identity=identity, expires_delta=timedelta(minutes=20))  # Changed to 20 minutes
            if not access_token:
                raise ValueError("Failed to generate JWT")
        except Exception as e:
            print(f"JWT creation error: {str(e)}")
            return jsonify({"message": "Failed to generate access token", "error": str(e)}), 500

        print(f"Login successful for user: {email}")
        # Return token and user info
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "user_type": user.user_type
            }
        }), 200

    except SQLAlchemyError as e:
        print(f"Database error during login: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"message": "Database error occurred", "error": str(e)}), 500

    except ValueError as e:
        print(f"Validation error during login: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"message": "Validation error", "error": str(e)}), 400

    except Exception as e:
        print(f"Unexpected login error: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500
    
    
    
    

# Logout and revoke JWT
@users_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']
        if not jti:
            print("No JTI found in JWT")
            return jsonify({"message": "Invalid token: JTI missing"}), 400

        from app import blacklist  # Import blacklist from __init__.py
        print(f"Revoking token with JTI: {jti}")
        blacklist.add(jti)

        print(f"Token revoked successfully: {jti}")
        return jsonify({"message": "Logged out successfully"}), 200

    except KeyError as e:
        print(f"JWT parsing error during logout: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"message": "Invalid token structure", "error": str(e)}), 400

    except Exception as e:
        print(f"Unexpected logout error: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"message": "An error occurred during logout", "error": str(e)}), 500

# Protected dashboard endpoint
@users_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    try:
        current_user = get_jwt_identity()
        if not current_user:
            print("No user identity found in JWT")
            return jsonify({"message": "Invalid token: No user identity"}), 401

        print(f"Accessing dashboard for user: {current_user.get('email', 'unknown')}")
        if current_user['user_type'] != 'admin':
            print(f"User {current_user['email']} is not an admin, user_type: {current_user['user_type']}")
            return jsonify({"message": "Unauthorized: Admin access required"}), 403

        return jsonify({
            "message": "Welcome to the admin dashboard",
            "user": current_user
        }), 200

    except KeyError as e:
        print(f"JWT identity error during dashboard access: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"message": "Invalid user data in token", "error": str(e)}), 400

    except Exception as e:
        print(f"Unexpected dashboard error: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"message": "An error occurred accessing dashboard", "error": str(e)}), 500
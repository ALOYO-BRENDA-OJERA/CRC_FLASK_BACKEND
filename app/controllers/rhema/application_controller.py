from flask import Blueprint, request, jsonify
from app.models.Rhema.application import Application
from app.extensions import db
import re

# Create Blueprint with clean URL prefix
application_bp = Blueprint('applications', __name__, url_prefix='/api/v1/applications')

def validate_email(email):
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format (basic international format)."""
    pattern = r'^\+?[\d\s-]{10,15}$'
    return re.match(pattern, phone) is not None

def validate_statement(statement):
    """Validate statement word count (100-200 words)."""
    words = statement.split()
    return 100 <= len(words) <= 200

@application_bp.route('/create', methods=['POST'])
def create_application():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided", "error": "Missing payload"}), 400

        # Extract and validate required fields
        required_fields = {
            'firstName': data.get('firstName'),
            'lastName': data.get('lastName'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'address': data.get('address'),
            'city': data.get('city'),
            'country': data.get('country'),
            'statement': data.get('statement')
        }
        for field_name, value in required_fields.items():
            if not value or value.strip() == '':
                return jsonify({"message": f"{field_name} is required", "error": "Missing field"}), 400

        # Validate email
        if not validate_email(required_fields['email']):
            return jsonify({"message": "Invalid email format", "error": "Validation error"}), 400

        # Validate phone
        if not validate_phone(required_fields['phone']):
            return jsonify({"message": "Invalid phone number format", "error": "Validation error"}), 400

        # Validate statement
        if not validate_statement(required_fields['statement']):
            return jsonify({"message": "Statement must be between 100 and 200 words", "error": "Validation error"}), 400

        # Validate hearAbout (optional)
        hear_about = data.get('hearAbout')
        valid_hear_about = ['', 'friend', 'church', 'social', 'website', 'other']
        if hear_about and hear_about not in valid_hear_about:
            return jsonify({"message": "Invalid hearAbout value", "error": "Validation error"}), 400

        # Create application
        application = Application(
            first_name=required_fields['firstName'],
            last_name=required_fields['lastName'],
            email=required_fields['email'],
            phone=required_fields['phone'],
            address=required_fields['address'],
            city=required_fields['city'],
            country=required_fields['country'],
            foundation_school=data.get('foundationSchool', False),
            hear_about=hear_about,
            statement=required_fields['statement']
        )

        db.session.add(application)
        db.session.commit()

        return jsonify({
            "message": "Application created successfully",
            "data": {
                "id": application.id,
                "first_name": application.first_name,
                "last_name": application.last_name,
                "email": application.email,
                "phone": application.phone,
                "address": application.address,
                "city": application.city,
                "country": application.country,
                "foundation_school": application.foundation_school,
                "hear_about": application.hear_about,
                "statement": application.statement,
                "submitted_at": application.submitted_at
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@application_bp.route('/get_all', methods=['GET'])
def get_all_applications():
    try:
        applications = Application.query.all()
        if applications:
            result = [{
                "id": app.id,
                "first_name": app.first_name,
                "last_name": app.last_name,
                "email": app.email,
                "phone": app.phone,
                "address": app.address,
                "city": app.city,
                "country": app.country,
                "foundation_school": app.foundation_school,
                "hear_about": app.hear_about,
                "statement": app.statement,
                "submitted_at": app.submitted_at
            } for app in applications]
            return jsonify({"data": result}), 200

        return jsonify({"message": "No applications found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@application_bp.route('/<int:application_id>', methods=['GET'])
def get_application_by_id(application_id):
    try:
        application = Application.query.get(application_id)
        if application:
            return jsonify({
                "data": {
                    "id": application.id,
                    "first_name": application.first_name,
                    "last_name": application.last_name,
                    "email": application.email,
                    "phone": application.phone,
                    "address": application.address,
                    "city": application.city,
                    "country": application.country,
                    "foundation_school": application.foundation_school,
                    "hear_about": application.hear_about,
                    "statement": application.statement,
                    "submitted_at": application.submitted_at
                }
            }), 200

        return jsonify({"message": "Application not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@application_bp.route('/<int:application_id>', methods=['PUT'])
def update_application_by_id(application_id):
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({"message": "Application not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided", "error": "Missing payload"}), 400

        # Update fields if provided, with validation
        if 'firstName' in data:
            if not data['firstName'] or data['firstName'].strip() == '':
                return jsonify({"message": "firstName is required", "error": "Missing field"}), 400
            application.first_name = data['firstName']

        if 'lastName' in data:
            if not data['lastName'] or data['lastName'].strip() == '':
                return jsonify({"message": "lastName is required", "error": "Missing field"}), 400
            application.last_name = data['lastName']

        if 'email' in data:
            if not data['email'] or data['email'].strip() == '':
                return jsonify({"message": "email is required", "error": "Missing field"}), 400
            if not validate_email(data['email']):
                return jsonify({"message": "Invalid email format", "error": "Validation error"}), 400
            application.email = data['email']

        if 'phone' in data:
            if not data['phone'] or data['phone'].strip() == '':
                return jsonify({"message": "phone is required", "error": "Missing field"}), 400
            if not validate_phone(data['phone']):
                return jsonify({"message": "Invalid phone number format", "error": "Validation error"}), 400
            application.phone = data['phone']

        if 'address' in data:
            if not data['address'] or data['address'].strip() == '':
                return jsonify({"message": "address is required", "error": "Missing field"}), 400
            application.address = data['address']

        if 'city' in data:
            if not data['city'] or data['city'].strip() == '':
                return jsonify({"message": "city is required", "error": "Missing field"}), 400
            application.city = data['city']

        if 'country' in data:
            if not data['country'] or data['country'].strip() == '':
                return jsonify({"message": "country is required", "error": "Missing field"}), 400
            application.country = data['country']

        if 'statement' in data:
            if not data['statement'] or data['statement'].strip() == '':
                return jsonify({"message": "statement is required", "error": "Missing field"}), 400
            if not validate_statement(data['statement']):
                return jsonify({"message": "Statement must be between 100 and 200 words", "error": "Validation error"}), 400
            application.statement = data['statement']

        if 'foundationSchool' in data:
            application.foundation_school = data['foundationSchool']

        if 'hearAbout' in data:
            valid_hear_about = ['', 'friend', 'church', 'social', 'website', 'other']
            if data['hearAbout'] and data['hearAbout'] not in valid_hear_about:
                return jsonify({"message": "Invalid hearAbout value", "error": "Validation error"}), 400
            application.hear_about = data['hearAbout']

        db.session.commit()

        return jsonify({
            "message": "Application updated successfully",
            "data": {
                "id": application.id,
                "first_name": application.first_name,
                "last_name": application.last_name,
                "email": application.email,
                "phone": application.phone,
                "address": application.address,
                "city": application.city,
                "country": application.country,
                "foundation_school": application.foundation_school,
                "hear_about": application.hear_about,
                "statement": application.statement,
                "submitted_at": application.submitted_at
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@application_bp.route('/<int:application_id>', methods=['DELETE'])
def delete_application_by_id(application_id):
    try:
        application = Application.query.get(application_id)
        if not application:
            return jsonify({"message": "Application not found"}), 404

        db.session.delete(application)
        db.session.commit()

        return jsonify({
            "message": "Application deleted successfully",
            "data": {
                "id": application_id
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@application_bp.route('/count', methods=['GET'])
def get_application_count():
    try:
        count = Application.query.count()
        return jsonify({"total": count}), 200
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500
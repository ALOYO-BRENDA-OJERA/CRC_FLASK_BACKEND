from flask import Blueprint, request, jsonify
from app.models.home.believers_model import NewBeliever
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Blueprint setup
new_believer_bp = Blueprint('new_believer', __name__, url_prefix='/api/v1/new-believers')

# CREATE
@new_believer_bp.route('/create', methods=['POST'])
def create_new_believer():
    try:
        data = request.get_json()
        new_believer = NewBeliever(
            full_name=data.get('full_name'),
            contact=data.get('contact'),
            email=data.get('email'),
            residence=data.get('residence'),
            date_saved=datetime.utcnow()
        )
        db.session.add(new_believer)
        db.session.commit()

        return jsonify({
            "message": "New believer created successfully",
            "data": {
                "id": new_believer.id,
                "full_name": new_believer.full_name,
                "contact": new_believer.contact,
                "email": new_believer.email,
                "residence": new_believer.residence,
                "date_saved": new_believer.date_saved,
                "created_at": new_believer.created_at,
                "updated_at": new_believer.updated_at
            }
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error occurred", "error": str(e)}), 500

# READ ALL
@new_believer_bp.route('/get_all', methods=['GET'])
def get_all_new_believers():
    try:
        believers = NewBeliever.query.all()
        if believers:
            result = [{
                "id": b.id,
                "full_name": b.full_name,
                "contact": b.contact,
                "email": b.email,
                "residence": b.residence,
                "date_saved": b.date_saved,
                "created_at": b.created_at,
                "updated_at": b.updated_at
            } for b in believers]

            return jsonify({"data": result}), 200

        return jsonify({"message": "No new believers found"}), 404

    except SQLAlchemyError as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# READ ONE
@new_believer_bp.route('/<int:believer_id>', methods=['GET'])
def get_new_believer_by_id(believer_id):
    try:
        believer = NewBeliever.query.get(believer_id)
        if believer:
            return jsonify({
                "data": {
                    "id": believer.id,
                    "full_name": believer.full_name,
                    "contact": believer.contact,
                    "email": believer.email,
                    "residence": believer.residence,
                    "date_saved": believer.date_saved,
                    "created_at": believer.created_at,
                    "updated_at": believer.updated_at
                }
            }), 200

        return jsonify({"message": "New believer not found"}), 404

    except SQLAlchemyError as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

# UPDATE
@new_believer_bp.route('/<int:believer_id>', methods=['PUT'])
def update_new_believer_by_id(believer_id):
    try:
        believer = NewBeliever.query.get(believer_id)
        if not believer:
            return jsonify({"message": "New believer not found"}), 404

        data = request.get_json()
        believer.full_name = data.get('full_name', believer.full_name)
        believer.contact = data.get('contact', believer.contact)
        believer.email = data.get('email', believer.email)
        believer.residence = data.get('residence', believer.residence)
        db.session.commit()

        return jsonify({
            "message": "New believer updated successfully",
            "data": {
                "id": believer.id,
                "full_name": believer.full_name,
                "contact": believer.contact,
                "email": believer.email,
                "residence": believer.residence,
                "date_saved": believer.date_saved,
                "created_at": believer.created_at,
                "updated_at": believer.updated_at
            }
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error updating believer", "error": str(e)}), 500

# DELETE
@new_believer_bp.route('/<int:believer_id>', methods=['DELETE'])
def delete_new_believer_by_id(believer_id):
    try:
        believer = NewBeliever.query.get(believer_id)
        if not believer:
            return jsonify({"message": "New believer not found"}), 404

        db.session.delete(believer)
        db.session.commit()

        return jsonify({
            "message": "New believer deleted successfully",
            "data": {"id": believer_id}
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting believer", "error": str(e)}), 500

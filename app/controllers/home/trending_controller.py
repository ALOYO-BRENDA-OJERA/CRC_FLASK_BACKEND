from flask import Blueprint, request, jsonify
from app.models.home.trending_nows_model import TrendingNow
from app.extensions import db

# Create Blueprint with cleaner URL prefix
trending_now_bp = Blueprint('trending', __name__, url_prefix='/api/v1/trending')

@trending_now_bp.route('/create', methods=['POST'])
def create_trending_item():
    try:
        data = request.get_json()
        trending_item = TrendingNow(
            description=data.get('description'),
            date=data.get('date')
        )
        db.session.add(trending_item)
        db.session.commit()

        return jsonify({
            "message": "Trending item created successfully",
            "data": {
                "id": trending_item.id,
                "description": trending_item.description,
                "date": trending_item.date,
                "created_at": trending_item.created_at,
                "updated_at": trending_item.updated_at
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@trending_now_bp.route('/get_all', methods=['GET'])
def get_all_trending_items():
    try:
        trending_items = TrendingNow.query.all()
        if trending_items:
            result = [{
                "id": item.id,
                "description": item.description,
                "date": item.date,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            } for item in trending_items]
            return jsonify({"data": result}), 200

        return jsonify({"message": "No trending items found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@trending_now_bp.route('/<int:trending_id>', methods=['GET'])
def get_trending_item_by_id(trending_id):
    try:
        item = TrendingNow.query.get(trending_id)
        if item:
            return jsonify({
                "data": {
                    "id": item.id,
                    "description": item.description,
                    "date": item.date,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at
                }
            }), 200

        return jsonify({"message": "Trending item not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@trending_now_bp.route('/<int:trending_id>', methods=['PUT'])
def update_trending_item_by_id(trending_id):
    try:
        item = TrendingNow.query.get(trending_id)
        if not item:
            return jsonify({"message": "Trending item not found"}), 404

        data = request.get_json()
        item.description = data.get('description', item.description)
        item.date = data.get('date', item.date)
        db.session.commit()

        return jsonify({
            "message": "Trending item updated successfully",
            "data": {
                "id": item.id,
                "description": item.description,
                "date": item.date,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@trending_now_bp.route('/<int:trending_id>', methods=['DELETE'])
def delete_trending_item_by_id(trending_id):
    try:
        item = TrendingNow.query.get(trending_id)
        if not item:
            return jsonify({"message": "Trending item not found"}), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({
            "message": "Trending item deleted successfully",
            "data": {
                "id": trending_id
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error occurred", "error": str(e)}), 500
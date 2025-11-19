from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

kb_admin_bp = Blueprint('kb_admin', __name__)

@kb_admin_bp.route('/articles', methods=['GET'])
@jwt_required()
def get_articles():
    # Check if user has admin role
    current_user = get_jwt_identity()
    
    # Simple role check
    if current_user != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    return jsonify({
        "message": "KB admin articles endpoint", 
        "user": current_user,
        "articles": ["KB001", "KB002"]
    }), 200

@kb_admin_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "KB Admin route is working!"}), 200
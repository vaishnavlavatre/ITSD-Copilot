from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

# Import our new auth service
from ..services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        # Use our auth service
        user = auth_service.authenticate(username, password)
        if user:
            # Create access token
            access_token = create_access_token(
                identity=username,
                expires_delta=datetime.timedelta(hours=24)
            )
            
            return jsonify({
                "access_token": access_token,
                "user": user
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        current_user = get_jwt_identity()
        user_data = auth_service.get_user(current_user)
        
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Auth route is working!"}), 200
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_feedback():
    try:
        data = request.get_json()
        
        query = data.get('query', '')
        response = data.get('response', '')
        was_helpful = data.get('was_helpful', False)
        user_feedback = data.get('user_feedback', '')
        
        # Create feedback entry
        feedback_entry = {
            "query": query,
            "response": response,
            "was_helpful": was_helpful,
            "user_feedback": user_feedback,
            "timestamp": datetime.now().isoformat()
        }
        
        # For now, just print the feedback (in real app, save to database)
        print(f"📝 Feedback received: {feedback_entry}")
        
        return jsonify({
            "message": "Feedback submitted successfully", 
            "feedback": feedback_entry
        }), 200
        
    except Exception as e:
        print(f"Error in submit_feedback: {str(e)}")
        return jsonify({"error": str(e)}), 500

@feedback_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Feedback route is working!"}), 200
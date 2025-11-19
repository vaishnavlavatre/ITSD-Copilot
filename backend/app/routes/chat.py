from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

# Import our services
from ..services.nlp_engine import NlpEngine
from ..services.knowledge_service import KnowledgeService
from ..services.automation_service import AutomationService

# Create blueprint
chat_bp = Blueprint('chat', __name__)

# Initialize services
nlp_engine = NlpEngine()

# Get the knowledge base file path - FIXED PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
project_root = os.path.dirname(backend_dir)
kb_file = os.path.join(project_root, 'knowledge_base', 'ford_kb.json')

print(f"Looking for KB file at: {kb_file}")

# Check if file exists, if not use unix_kb.json as fallback
if not os.path.exists(kb_file):
    kb_file = os.path.join(project_root, 'knowledge_base', 'unix_kb.json')
    print(f"Ford KB not found, using fallback: {kb_file}")

knowledge_service = KnowledgeService(kb_file)
automation_service = AutomationService()

@chat_bp.route('/query', methods=['POST'])
@jwt_required()
def chat_query():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({"error": "Query is required"}), 400
        
        print(f"Processing query: {user_query}")
        
        # Process query with NLP
        intent, entities = nlp_engine.process_query(user_query)
        print(f"Intent: {intent}, Entities: {entities}")
        
        # Search knowledge base with user query for better matching
        kb_results = knowledge_service.search_knowledge(intent, entities, user_query)
        print(f"KB Results: {kb_results}")
        
        # Generate automation suggestions
        automation_suggestions = automation_service.generate_command_sequence(intent, entities)
        
        # Format response
        response_text = knowledge_service.format_response(kb_results, automation_suggestions)
        
        # Prepare final response
        response = {
            "intent": intent,
            "entities": entities,
            "response": response_text,
            "automation_suggestions": automation_suggestions,
            "kb_matches": list(kb_results.keys()) if kb_results else []
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in chat_query: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@chat_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Chat route is working!"}), 200
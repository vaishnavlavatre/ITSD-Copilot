from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-change-in-production'
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    
    # Import and register blueprints with error handling
    blueprints = [
        ('auth', '/auth'),
        ('chat', '/chat'),
        ('feedback', '/feedback'),
        ('kb_admin', '/kb-admin')
    ]
    
    for bp_name, url_prefix in blueprints:
        try:
            # Dynamic import
            module = __import__(f'app.routes.{bp_name}', fromlist=[f'{bp_name}_bp'])
            blueprint = getattr(module, f'{bp_name}_bp')
            app.register_blueprint(blueprint, url_prefix=url_prefix)
            print(f"✓ Registered blueprint: {bp_name} at {url_prefix}")
        except ImportError as e:
            print(f"⚠️  Warning: Could not import {bp_name} blueprint: {e}")
        except AttributeError as e:
            print(f"⚠️  Warning: Could not find blueprint for {bp_name}: {e}")
    
    # Add a default route for testing
    @app.route('/')
    def home():
        return {
            "message": "ITSD Admin Copilot API is running!",
            "endpoints": {
                "auth": "/auth/*",
                "chat": "/chat/*", 
                "feedback": "/feedback/*",
                "kb_admin": "/kb-admin/*"
            }
        }
    
    return app
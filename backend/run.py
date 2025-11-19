import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

try:
    from app import create_app
    print("✓ Successfully imported create_app from app")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Current Python path:", sys.path)
    print("Current directory:", os.getcwd())
    print("Files in current directory:", os.listdir('.'))
    
    # Try to check if app folder exists
    if os.path.exists('app'):
        print("✓ 'app' folder exists")
        print("Files in app folder:", os.listdir('app'))
    else:
        print("✗ 'app' folder does not exist")
    
    sys.exit(1)

app = create_app()

if __name__ == '__main__':
    print("🚀 Starting ITSD Admin Copilot Server...")
    print("📍 Available at: http://localhost:5000")
    print("📋 Test endpoints:")
    print("   - http://localhost:5000/chat/test")
    print("   - http://localhost:5000/auth/test")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
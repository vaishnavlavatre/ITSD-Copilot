
import json
import os

def verify_kb_file():
    kb_file = 'ford_kb.json'
    
    print(f"🔍 Verifying {kb_file}...")
    
    # Check if file exists
    if not os.path.exists(kb_file):
        print(f"❌ File {kb_file} does not exist!")
        return False
    
    # Check file size
    file_size = os.path.getsize(kb_file)
    print(f"📁 File size: {file_size} bytes")
    
    if file_size == 0:
        print("❌ File is empty!")
        return False
    
    # Try to parse JSON
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON is valid!")
        
        # Check structure
        required_sections = ['intents', 'commands', 'troubleshooting', 'articles', 'faq']
        for section in required_sections:
            if section in data:
                print(f"✅ Section '{section}' found")
            else:
                print(f"❌ Missing section '{section}'")
        
        print(f"📚 Articles: {len(data.get('articles', {}))}")
        print(f"❓ FAQ entries: {len(data.get('faq', {}))}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if verify_kb_file():
        print("\n🎉 KB file is ready to use!")
    else:
        print("\n⚠️ Please fix the KB file issues above.")
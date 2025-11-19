import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/itsd_copilot'
    KNOWLEDGE_BASE_FILE = os.environ.get('KNOWLEDGE_BASE_FILE') or '../knowledge_base/unix_kb.json'
    FEEDBACK_FILE = os.environ.get('FEEDBACK_FILE') or '../knowledge_base/feedback_log.json'
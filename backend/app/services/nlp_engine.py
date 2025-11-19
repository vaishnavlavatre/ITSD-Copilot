import re
import json
from typing import Dict, List, Tuple

class NlpEngine:
    def __init__(self):
        # Enhanced intent patterns
        self.intent_patterns = {
            'command_syntax': [
                r'how.*command', r'what.*command', r'syntax.*',
                r'how.*run', r'what.*syntax', r'how.*use.*command',
                r'explain.*command', r'what does.*command.*do',
                r'example of.*command', r'usage of.*command'
            ],
            'troubleshooting': [
                r'error', r'fix', r'problem', r'issue',
                r'not working', r'failed', r'broken', r'won\'t start',
                r'cannot', r'can\'t', r'unable to', r'permission denied',
                r'command not found', r'no such file'
            ],
            'status_check': [
                r'status', r'check', r'is.*up', r'is.*down',
                r'running', r'stopped', r'how.*check',
                r'system health', r'resource usage', r'monitor'
            ],
            'user_management': [
                r'user', r'add user', r'create user', r'delete user',
                r'password', r'permission', r'group', r'sudo',
                r'user account', r'add to group'
            ],
            'process_management': [
                r'process', r'kill', r'stop', r'start',
                r'restart', r'service', r'background',
                r'daemon', r'ps', r'killall'
            ],
            'file_management': [
                r'file', r'directory', r'folder', r'permission',
                r'chmod', r'chown', r'copy', r'move', r'delete',
                r'find.*file', r'search.*file'
            ]
        }
        
        # Enhanced entity patterns
        self.entity_patterns = {
            'server_name': r'server-[a-zA-Z0-9-]+|prod-|staging-|dev-',
            'username': r'user[a-zA-Z0-9_]*|\b[a-z][a-z0-9_]{2,31}\b',
            'error_code': r'error[A-Z0-9]*|ERR[A-Z0-9]*|permission denied|command not found|no such file',
            'software_name': r'(apache|nginx|ssh|mysql|postgresql|docker|kubernetes|k8s|python|java)',
            'command_name': r'(cd|ls|grep|find|chmod|chown|ps|kill|df|du|top|htop|free|uname|who|w)',
            'file_path': r'/[/a-zA-Z0-9_.-]+|\~?/[a-zA-Z0-9_/. -]+'
        }

    def extract_intent(self, text: str) -> str:
        """Extract intent from user query with confidence scoring"""
        text_lower = text.lower()
        scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    score += 1
            scores[intent] = score
        
        # Get intent with highest score
        best_intent = max(scores, key=scores.get)
        return best_intent if scores[best_intent] > 0 else 'general_query'

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from user query"""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Remove duplicates and filter empty matches
                unique_matches = list(set([match for match in matches if match.strip()]))
                if unique_matches:
                    entities[entity_type] = unique_matches
        
        return entities

    def process_query(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        """Process user query and return intent and entities"""
        intent = self.extract_intent(text)
        entities = self.extract_entities(text)
        
        print(f"🔍 NLP Analysis: '{text}' -> Intent: {intent}, Entities: {entities}")
        
        return intent, entities

# Test the enhanced NLP
if __name__ == "__main__":
    nlp = NlpEngine()
    test_queries = [
        "How do I check disk space using df command?",
        "Permission denied error when accessing /var/log",
        "How to restart apache service on server-web-01",
        "Create a new user named john with sudo permissions"
    ]
    
    for query in test_queries:
        intent, entities = nlp.process_query(query)
        print(f"Query: {query}")
        print(f"Intent: {intent}")
        print(f"Entities: {entities}")
        print("---")
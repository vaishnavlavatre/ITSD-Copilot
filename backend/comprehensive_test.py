import json
import os
from typing import Dict, List, Optional
import re

class KnowledgeService:
    def __init__(self, kb_file: str):
        self.kb_file = kb_file
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self) -> Dict:
        """Load knowledge base from JSON file"""
        try:
            with open(self.kb_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Knowledge base file {self.kb_file} not found. Creating default structure.")
            return self.create_default_kb()

    def search_knowledge(self, intent: str, entities: Dict, user_query: str = "") -> Optional[Dict]:
        """Search knowledge base for relevant information"""
        results = {}
        
        # Search by intent in structured sections
        if intent in self.knowledge_base.get('intents', {}):
            results['intent_matches'] = self.knowledge_base['intents'][intent]
        
        # Search for command syntax
        if 'command_name' in entities:
            for command in entities['command_name']:
                if command in self.knowledge_base.get('commands', {}):
                    if 'command_matches' not in results:
                        results['command_matches'] = {}
                    results['command_matches'][command] = self.knowledge_base['commands'][command]
        
        # Search troubleshooting
        if intent == 'troubleshooting' and 'error_code' in entities:
            for error in entities['error_code']:
                if error in self.knowledge_base.get('troubleshooting', {}):
                    if 'troubleshooting_matches' not in results:
                        results['troubleshooting_matches'] = {}
                    results['troubleshooting_matches'][error] = self.knowledge_base['troubleshooting'][error]
        
        # Search FAQ using the user query
        if user_query:
            faq_results = self.search_faq(user_query)
            if faq_results:
                results['faq_matches'] = faq_results
        
        # Search articles by keywords
        article_results = self.search_articles(user_query, entities)
        if article_results:
            results['article_matches'] = article_results
        
        return results if results else None

    def search_faq(self, user_query: str) -> Dict:
        """Search FAQ using keyword matching"""
        query_lower = user_query.lower()
        matches = {}
        
        if 'faq' in self.knowledge_base:
            for faq_id, faq_data in self.knowledge_base['faq'].items():
                # Check question
                if faq_data.get('question', '').lower() in query_lower:
                    matches[faq_id] = faq_data
                    continue
                
                # Check variations
                variations = faq_data.get('variations', [])
                for variation in variations:
                    if variation.lower() in query_lower:
                        matches[faq_id] = faq_data
                        break
        
        return matches

    def search_articles(self, user_query: str, entities: Dict) -> Dict:
        """Search articles by keywords and entities"""
        query_lower = user_query.lower()
        matches = {}
        
        if 'articles' in self.knowledge_base:
            for article_id, article_data in self.knowledge_base['articles'].items():
                score = 0
                
                # Check title
                title = article_data.get('title', '').lower()
                if any(word in title for word in query_lower.split()):
                    score += 2
                
                # Check tags
                tags = article_data.get('tags', [])
                for tag in tags:
                    if tag.lower() in query_lower:
                        score += 3
                    if entities and any(tag.lower() in str(entity).lower() for entity_list in entities.values() for entity in entity_list):
                        score += 2
                
                # Check content for main keywords
                content = article_data.get('content', '').lower()
                if any(keyword in content for keyword in query_lower.split() if len(keyword) > 3):
                    score += 1
                
                if score >= 2:  # Threshold for considering it a match
                    matches[article_id] = {
                        'title': article_data.get('title', ''),
                        'content': article_data.get('content', ''),
                        'score': score
                    }
        
        # Sort by score and return top 3
        sorted_matches = dict(sorted(matches.items(), key=lambda x: x[1]['score'], reverse=True)[:3])
        return sorted_matches

    def format_response(self, kb_results, automation_suggestions=None):
        """Format the response based on available data"""
        if not kb_results and not automation_suggestions:
            return "I'm not sure how to help with that. Could you provide more details?"
        
        response_parts = []
        
        if kb_results:
            # FAQ matches (highest priority)
            if 'faq_matches' in kb_results:
                for faq_id, faq_data in kb_results['faq_matches'].items():
                    response_parts.append(f"**{faq_data.get('question', 'Help')}**")
                    response_parts.append(f"{faq_data.get('answer', '')}")
            
            # Article matches
            if 'article_matches' in kb_results:
                response_parts.append("\n**Related Knowledge Articles:**")
                for article_id, article_data in kb_results['article_matches'].items():
                    response_parts.append(f"\n📖 **{article_data['title']}**")
                    # Show first 200 characters of content
                    content_preview = article_data['content'][:200] + "..." if len(article_data['content']) > 200 else article_data['content']
                    response_parts.append(f"{content_preview}")
            
            # Command help
            if 'command_matches' in kb_results:
                response_parts.append("\n**Command Help:**")
                for cmd, info in kb_results['command_matches'].items():
                    response_parts.append(f"- `{cmd}`: {info}")
            
            # Troubleshooting
            if 'troubleshooting_matches' in kb_results:
                response_parts.append("\n**Troubleshooting:**")
                for error, solution in kb_results['troubleshooting_matches'].items():
                    response_parts.append(f"- **{error}**: {solution}")
        
        if automation_suggestions:
            response_parts.append("\n**Recommended Steps:**")
            for step in automation_suggestions:
                response_parts.append(f"- {step['description']}")
                response_parts.append(f"  Command: `{step['command']}`")
        
        return "\n".join(response_parts)

    def create_default_kb(self) -> Dict:
        """Create default knowledge base structure"""
        default_kb = {
            "intents": {},
            "commands": {},
            "troubleshooting": {},
            "articles": {},
            "faq": {}
        }
        
        # Save the default KB
        with open(self.kb_file, 'w', encoding='utf-8') as f:
            json.dump(default_kb, f, indent=2, ensure_ascii=False)
        
        return default_kb
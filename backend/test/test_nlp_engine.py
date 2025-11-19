# backend/tests/test_nlp_engine.py
def test_intent_classification():
    nlp_engine = NlpEngine()
    intent, entities = nlp_engine.process_query("How do I check disk space?")
    assert intent == "command_syntax"
    assert "command_name" in entities

def test_entity_extraction():
    nlp_engine = NlpEngine()
    intent, entities = nlp_engine.process_query("Fix permission denied error on server-web-01")
    assert "error_code" in entities
    assert "server_name" in entities
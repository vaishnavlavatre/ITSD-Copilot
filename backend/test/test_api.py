# backend/tests/test_api.py
def test_chat_endpoint():
    client = app.test_client()
    response = client.post('/chat/query', 
                         json={'query': 'How to restart Apache?'},
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert 'intent' in data
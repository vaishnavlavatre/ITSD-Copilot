class AuthService:
    def __init__(self):
        # Simple user database (in real app, use proper database)
        self.users = {
            "admin": {
                "password": "admin123", 
                "role": "admin", 
                "name": "System Administrator"
            },
            "agent1": {
                "password": "agent123", 
                "role": "agent", 
                "name": "John Doe"
            },
            "agent2": {
                "password": "agent123", 
                "role": "agent", 
                "name": "Jane Smith"
            }
        }

    def authenticate(self, username: str, password: str) -> dict:
        """Authenticate user and return user data if valid"""
        if username in self.users and self.users[username]['password'] == password:
            return {
                "username": username,
                "name": self.users[username]['name'],
                "role": self.users[username]['role']
            }
        return None

    def get_user(self, username: str) -> dict:
        """Get user data by username"""
        if username in self.users:
            return {
                "username": username,
                "name": self.users[username]['name'],
                "role": self.users[username]['role']
            }
        return None
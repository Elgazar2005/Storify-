class User:
    def __init__(self, id, username, email, password, role):
        self.id = int(id)
        self.username = username
        self.email = email
        self.password = password
        self.role = role 
    def __repr__(self):
        return f"<User {self.id} - {self.username} ({self.role})>"

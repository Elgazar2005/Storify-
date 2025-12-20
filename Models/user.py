class User:
    def __init__(self, id, username, email, password, role, store_name=""):
        self.id = int(id)
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.store_name = store_name

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "store_name": self.store_name
        }

    def __repr__(self):
        return f"<User {self.id} - {self.username} ({self.role})>"

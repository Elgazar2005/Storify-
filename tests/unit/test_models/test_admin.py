from Models.user import User

class Admin(User):
    def __init__(self, id, username, email, password):
        super().__init__(id, username, email, password, role="admin")

    def __repr__(self):
        return f"<Admin {self.id} - {self.username}>"

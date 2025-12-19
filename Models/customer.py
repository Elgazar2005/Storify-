from Models.user import User

class Customer(User):
    def __init__(self, id, username, email, password):
        super().__init__(id, username, email, password, role="customer")

    def __repr__(self):
        return f"<Customer {self.id} - {self.username}>"
from Models.user import User

class Seller(User):
    def __init__(self, id, username, email, password, store_name):
        super().__init__(id, username, email, password, role="seller")
        self.store_name = store_name

    def __repr__(self):
        return f"<Seller {self.id} - {self.store_name}>"

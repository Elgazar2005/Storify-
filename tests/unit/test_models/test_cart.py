class Cart:
    def __init__(self, id, user_id, status="open"):
        self.id = int(id)
        self.user_id = int(user_id)
        self.status = status

    def __repr__(self):
        return f"<Cart {self.id} - User {self.user_id} - {self.status}>"



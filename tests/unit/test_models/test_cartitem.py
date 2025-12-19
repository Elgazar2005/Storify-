class CartItem:
    def __init__(self, id, cart_id, product_id, quantity):
        self.id = int(id)
        self.cart_id = int(cart_id)
        self.product_id = int(product_id)
        self.quantity = int(quantity)

    def __repr__(self):
        return f"<CartItem {self.id} (Cart {self.cart_id} - Product {self.product_id})>"

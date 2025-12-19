class OrderItem:
    def __init__(self, order_item_id, order_id, product_id, product_name, quantity, price,seller_id):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.seller_id = seller_id
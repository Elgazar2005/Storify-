class Order:
    def __init__(self, order_id, customer_id, created_at, status, total_amount):
        self.order_id = order_id
        self.customer_id = customer_id
        self.created_at = created_at
        self.status = status
        self.total_amount = total_amount
    def __repr__(self):
        return f"<Order {self.order_id} - Customer {self.customer_id} - {self.status}>"
from Models.order import Order

def test_order_creation():
    order = Order(1, 10, "2024-01-01", "pending", 250)

    assert order.order_id == 1
    assert order.customer_id == 10
    assert order.status == "pending"
    assert order.total_amount == 250

def test_order_repr():
    order = Order(1, 10, "2024-01-01", "pending", 250)
    assert repr(order) == "<Order 1 - Customer 10 - pending>"
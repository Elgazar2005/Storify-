from Models.orderitem import OrderItem

def test_order_item_creation():
    item = OrderItem(1, 2, 3, "Phone", 2, 500.0, 9)

    assert item.order_item_id == 1
    assert item.product_name == "Phone"
    assert item.quantity == 2
    assert item.price == 500.0
    assert item.seller_id == 9

def test_order_item_repr():
    item = OrderItem(1, 2, 3, "Phone", 2, 500.0, 9)
    assert repr(item) == "<OrderItem 1 - Phone (x2)>"

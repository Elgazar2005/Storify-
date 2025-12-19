from Models.cartitem import CartItem

def test_cart_item_creation():
    item = CartItem(1, 2, 3, 5)

    assert item.id == 1
    assert item.cart_id == 2
    assert item.product_id == 3
    assert item.quantity == 5

def test_cart_item_repr():
    item = CartItem(1, 2, 3, 5)
    assert repr(item) == "<CartItem 1 (Cart 2 - Product 3)>"
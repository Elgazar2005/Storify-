from Models.cart import Cart

def test_cart_creation():
    cart = Cart(1, 10)

    assert cart.id == 1
    assert cart.user_id == 10
    assert cart.status == "open"

def test_cart_repr():
    cart = Cart(1, 10, "open")
    assert repr(cart) == "<Cart 1 - User 10 - open>"

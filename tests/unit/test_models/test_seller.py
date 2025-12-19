from Models.seller import Seller

def test_seller_creation():
    seller = Seller(1, "shop1", "s@test.com", "1234", "My Store")

    assert seller.id == 1
    assert seller.username == "shop1"
    assert seller.store_name == "My Store"
    assert seller.role == "seller"

def test_seller_repr():
    seller = Seller(1, "shop1", "s@test.com", "1234", "My Store")
    assert repr(seller) == "<Seller 1 - My Store>"

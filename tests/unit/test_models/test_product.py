from Models.product import Product


def test_product_creation():
    product = Product(
        id=1,
        name="Laptop",
        description="Gaming laptop",
        price=15000,
        stock=5,
        image="laptop.png"
    )

    assert product.id == 1
    assert product.name == "Laptop"
    assert product.description == "Gaming laptop"
    assert product.price == 15000.0
    assert product.stock == 5
    assert product.image == "laptop.png"


def test_product_repr():
    product = Product(
        id=2,
        name="Phone",
        description="Smart phone",
        price=8000,
        stock=3,
        image="phone.png"
    )

    assert repr(product) == "<Product 2 - Phone>"

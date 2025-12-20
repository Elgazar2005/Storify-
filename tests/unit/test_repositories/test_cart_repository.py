import pytest
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository

TEST_USER_ID = 999


@pytest.fixture
def cart_repo():
    return CartRepository()


@pytest.fixture(scope="module")
def existing_product_id():
    """
    Get any existing product ID from products.csv
    """
    product_repo = ProductRepository()
    products = product_repo.get_all()

    assert len(products) > 0, "❌ No products found in products.csv for testing"
    return products[0].id


def test_add_to_cart(cart_repo, existing_product_id):
    cart_repo.add_to_cart(
        user_id=TEST_USER_ID,
        product_id=existing_product_id,
        quantity=2
    )

    cart, items = cart_repo.get_cart_with_products(TEST_USER_ID)

    assert cart is not None
    assert len(items) > 0
    assert items[0]["item"].quantity >= 2


def test_get_cart_with_products(cart_repo, existing_product_id):
    # ensure cart exists
    cart_repo.add_to_cart(
        user_id=TEST_USER_ID,
        product_id=existing_product_id,
        quantity=1
    )

    cart, items = cart_repo.get_cart_with_products(TEST_USER_ID)

    assert cart is not None
    assert isinstance(items, list)

    for row in items:
        assert "item" in row
        assert "product" in row
        assert row["product"] is not None


def test_remove_from_cart(cart_repo, existing_product_id):
    cart_repo.remove_from_cart(
        user_id=TEST_USER_ID,
        product_id=existing_product_id
    )

    cart, items = cart_repo.get_cart_with_products(TEST_USER_ID)

    if items:
        for row in items:
            assert row["item"].product_id != existing_product_id

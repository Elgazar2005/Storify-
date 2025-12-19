import os
import pytest
from repositories.product_repository import ProductRepository
from Models.product import Product

# path بتاع ملف test_products.csv
TEST_PRODUCTS_FILE = os.path.join(
    os.path.dirname(__file__),
    "../../data/test_products.csv"
)


def test_get_all_products():
    repo = ProductRepository(products_file_path=TEST_PRODUCTS_FILE)

    products = repo.get_all()

    assert isinstance(products, list)
    assert len(products) > 0
    assert isinstance(products[0], Product)


def test_get_product_by_id_found():
    repo = ProductRepository(products_file_path=TEST_PRODUCTS_FILE)

    product = repo.get_by_id(1)

    assert product is not None
    assert isinstance(product, Product)
    assert product.id == 1


def test_get_product_by_id_not_found():
    repo = ProductRepository(products_file_path=TEST_PRODUCTS_FILE)

    product = repo.get_by_id(999)

    assert product is None

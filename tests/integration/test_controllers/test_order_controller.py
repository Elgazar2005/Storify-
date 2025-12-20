import pytest

def mock_products():
    class Product:
        def __init__(self, id, name):
            self.id = id
            self.name = name

    return [
        Product(1, "Product 1"),
        Product(2, "Product 2"),
    ]


def test_list_products(client, monkeypatch):
    from repositories.repository_factory import RepositoryFactory

    product_repo = RepositoryFactory.get_product()

    monkeypatch.setattr(
        product_repo,
        "get_all",
        lambda: mock_products()
    )

    response = client.get("/products")
    assert response.status_code == 200


def test_product_details_success(client, monkeypatch):
    from repositories.repository_factory import RepositoryFactory

    product_repo = RepositoryFactory.get_product()
    products = mock_products()

    monkeypatch.setattr(
        product_repo,
        "get_by_id",
        lambda product_id: products[0] if product_id == 1 else None
    )

    response = client.get("/products/1")
    assert response.status_code == 200


def test_product_details_not_found(client, monkeypatch):
    from repositories.repository_factory import RepositoryFactory

    product_repo = RepositoryFactory.get_product()

    monkeypatch.setattr(
        product_repo,
        "get_by_id",
        lambda product_id: None
    )

    response = client.get("/products/999")
    assert response.status_code == 404

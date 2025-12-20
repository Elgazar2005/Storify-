import pytest
def login_as_seller(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["role"] = "seller"
class FakeProductRepo:
    def get_products_by_seller(self, seller_id):
        return []


class FakeOrderRepo:
    def get_orders_for_seller(self, seller_id):
        return []


class FakeNotificationRepo:
    def get_notifications_by_user(self, user_id):
        return []

def test_seller_dashboard_not_logged_in(client):
    response = client.get("/seller")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_seller_dashboard_logged_in(client, monkeypatch):
    login_as_seller(client)

    from repositories import repository_factory

    monkeypatch.setattr(
        repository_factory.RepositoryFactory,
        "get_product",
        lambda: FakeProductRepo()
    )
    monkeypatch.setattr(
        repository_factory.RepositoryFactory,
        "get_notification",
        lambda: FakeNotificationRepo()
    )

    response = client.get("/seller")
    assert response.status_code == 200


def test_seller_products_not_logged_in(client):
    response = client.get("/seller/products")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_seller_products_logged_in(client, monkeypatch):
    login_as_seller(client)

    from repositories import repository_factory

    monkeypatch.setattr(
        repository_factory.RepositoryFactory,
        "get_product",
        lambda: FakeProductRepo()
    )

    response = client.get("/seller/products")
    assert response.status_code == 200


def test_seller_orders_not_logged_in(client):
    response = client.get("/seller/orders")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_seller_orders_logged_in(client, monkeypatch):
    login_as_seller(client)

    from repositories import repository_factory

    monkeypatch.setattr(
        repository_factory.RepositoryFactory,
        "get_order",
        lambda: FakeOrderRepo()
    )

    response = client.get("/seller/orders")
    assert response.status_code == 200

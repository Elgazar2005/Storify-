import pytest
from flask import Flask
from controllers import admin_controller
from controllers.admin_controller import admin_bp



class FakeUser:
    def __init__(self, role):
        self.role = role


class FakeUserRepository:
    def get_all(self):
        return [
            FakeUser("admin"),
            FakeUser("seller"),
            FakeUser("customer"),
        ]


class FakeProductRepository:
    def get_all(self):
        return ["product1", "product2"]


@pytest.fixture
def app(monkeypatch):
    app = Flask(__name__)
    app.secret_key = "test_secret"
    app.register_blueprint(admin_bp)

    monkeypatch.setattr(admin_controller, "user_repo", FakeUserRepository())
    monkeypatch.setattr(admin_controller, "product_repo", FakeProductRepository())

    monkeypatch.setattr(
        admin_controller,
        "render_template",
        lambda *args, **kwargs: "OK"
    )

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def login_as_admin(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["role"] = "admin"



def test_admin_dashboard_redirect_if_not_admin(client):
    response = client.get("/admin")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_admin_dashboard_access_as_admin(client):
    login_as_admin(client)
    response = client.get("/admin")
    assert response.status_code == 200


def test_verify_sellers_access_as_admin(client):
    login_as_admin(client)
    response = client.get("/admin/verify_sellers")
    assert response.status_code == 200


def test_verify_products_access_as_admin(client):
    login_as_admin(client)
    response = client.get("/admin/verify_products")
    assert response.status_code == 200

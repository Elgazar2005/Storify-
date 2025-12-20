import pytest
from flask import Flask
from controllers.auth_controller import auth_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.secret_key = "test"
    app.register_blueprint(auth_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()


def test_login_success_customer(client):
    response = client.post(
        "/login",
        data={"email": "test@test.com", "password": "1234"},
        follow_redirects=False
    )
    assert response.status_code == 302


def test_login_success_seller(client):
    response = client.post(
        "/login",
        data={"email": "seller@test.com", "password": "1234"},
        follow_redirects=False
    )
    assert response.status_code == 302


def test_login_fail(client):
    response = client.post(
        "/login",
        data={"email": "wrong@test.com", "password": "0000"},
        follow_redirects=False
    )
    assert response.status_code == 401


def test_signup(client):
    response = client.post(
        "/signup",
        data={
            "username": "newuser",
            "email": "new@test.com",
            "password": "1234"
        },
        follow_redirects=False
    )
    assert response.status_code == 302

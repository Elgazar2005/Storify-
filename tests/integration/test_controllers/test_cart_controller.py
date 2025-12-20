import pytest
from flask import url_for

def test_view_cart(client):
    response = client.get("/cart")
    assert response.status_code == 200
    assert b"cart" in response.data or b"Cart" in response.data
def test_add_to_cart(client):
    response = client.post(
        "/cart/add/1",
        data={"quantity": 2},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert "/cart" in response.headers["Location"]
def test_remove_from_cart(client):
    response = client.post(
        "/cart/remove/1",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/cart" in response.headers["Location"]
def test_cart_after_add(client):
    client.post("/cart/add/1", data={"quantity": 1})
    response = client.get("/cart")
    assert response.status_code == 200

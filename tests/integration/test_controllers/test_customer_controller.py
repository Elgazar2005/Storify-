import pytest

# ---------- mocks ----------
class MockUser:
    def __init__(self, id, email):
        self.id = id
        self.email = email


def mock_users():
    return [
        MockUser(1, "test@test.com"),
        MockUser(2, "user@test.com"),
    ]


# ---------- tests ----------

def test_users_list(client, monkeypatch):
    from repositories.user_repository import UserRepository

    monkeypatch.setattr(
        UserRepository,
        "get_all",
        lambda self: mock_users()
    )

    response = client.get("/users")
    assert response.status_code == 200


def test_user_profile_success(client, monkeypatch):
    from repositories.user_repository import UserRepository

    monkeypatch.setattr(
        UserRepository,
        "get_by_id",
        lambda self, user_id: mock_users()[0] if user_id == 1 else None
    )

    response = client.get("/users/1")
    assert response.status_code == 200


def test_user_profile_not_found(client, monkeypatch):
    from repositories.user_repository import UserRepository

    monkeypatch.setattr(
        UserRepository,
        "get_by_id",
        lambda self, user_id: None
    )

    response = client.get("/users/99")
    assert response.status_code == 404

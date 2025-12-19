import os
from repositories.user_repository import UserRepository
from Models.user import User


def test_get_all_users():
    # path بتاع ملف الـ test data
    test_file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
        "test_users.csv"
    )

    repo = UserRepository(file_path=test_file_path)
    users = repo.get_all()

    assert isinstance(users, list)
    assert len(users) > 0
    assert isinstance(users[0], User)


def test_get_user_by_id_found():
    test_file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
        "test_users.csv"
    )

    repo = UserRepository(file_path=test_file_path)
    user = repo.get_by_id(1)

    assert user is not None
    assert isinstance(user, User)
    assert user.id == 1


def test_get_user_by_id_not_found():
    test_file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
        "test_users.csv"
    )

    repo = UserRepository(file_path=test_file_path)
    user = repo.get_by_id(999)

    assert user is None

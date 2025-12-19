from Models.user import User

def test_user_creation():
    user = User(1, "omar", "omar@test.com", "1234", "customer")

    assert user.id == 1
    assert user.username == "omar"
    assert user.email == "omar@test.com"
    assert user.password == "1234"
    assert user.role == "customer"

def test_user_repr():
    user = User(1, "omar", "omar@test.com", "1234", "customer")
    assert repr(user) == "<User 1 - omar (customer)>"
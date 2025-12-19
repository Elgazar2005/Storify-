from Models.customer import Customer

def test_customer_creation():
    customer = Customer(1, "ali", "ali@test.com", "1234")

    assert customer.id == 1
    assert customer.username == "ali"
    assert customer.email == "ali@test.com"
    assert customer.role == "customer"

def test_customer_repr():
    customer = Customer(1, "ali", "ali@test.com", "1234")
    assert repr(customer) == "<Customer 1 - ali>"

from repositories.repository_factory import RepositoryFactory
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository
from repositories.cart_repository import CartRepository
from repositories.order_repository import OrderRepository
from repositories.notification_repository import NotificationRepository

def test_get_user_repository():
    repo = RepositoryFactory.get_user()
    assert isinstance(repo, UserRepository)

def test_get_product_repository():
    repo = RepositoryFactory.get_product()
    assert isinstance(repo, ProductRepository)

def test_get_cart_repository():
    repo = RepositoryFactory.get_cart()
    assert isinstance(repo, CartRepository)

def test_get_order_repository():
    repo = RepositoryFactory.get_order()
    assert isinstance(repo, OrderRepository)

def test_get_notification_repository():
    repo = RepositoryFactory.get_notification()
    assert isinstance(repo, NotificationRepository)
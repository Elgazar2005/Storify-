from repositories.notification_repository import NotificationRepository
from repositories.order_repository import OrderRepository
from core.file_singletone import FileSingleton
from repositories.user_repository import UserRepository
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository

class RepositoryFactory:
    file = FileSingleton()
    @staticmethod
    def get_notification():
        return NotificationRepository(RepositoryFactory.file)
    @staticmethod
    def get_order():
        return OrderRepository(RepositoryFactory.file)
    @staticmethod
    def get_user():
        return UserRepository(RepositoryFactory.file)
    @staticmethod
    def get_cart():
        return CartRepository(RepositoryFactory.file)
    @staticmethod
    def get_product():
        return ProductRepository(RepositoryFactory.file)
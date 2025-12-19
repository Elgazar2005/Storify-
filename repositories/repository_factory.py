from repositories.notification_repository import NotificationRepository
from repositories.order_repository import OrderRepository
from core.file_singletone import FileSingleton
from repositories.user_repository import UserRepository
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository

class RepositoryFactory:
    @staticmethod
    def get_notification():
        return NotificationRepository
    @staticmethod
    def get_order():
        return OrderRepository
    @staticmethod
    def get_user():
        return UserRepository
    @staticmethod
    def get_cart():
        return CartRepository
    @staticmethod
    def get_product():
        return ProductRepository
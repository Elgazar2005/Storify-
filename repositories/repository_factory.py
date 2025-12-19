from repositories.notification_repository import NotificationRepository
from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from core.file_singletone import FileSingleton

class RepositoryFactory:
    file = FileSingleton()

    @staticmethod
    def get_user():
        return UserRepository(RepositoryFactory.file)

    @staticmethod
    def get_product():
        return ProductRepository(RepositoryFactory.file)

    @staticmethod
    def get_cart():
        return CartRepository() 

    @staticmethod
    def get_order():
        return OrderRepository()  

    @staticmethod
    def get_notification():
        return NotificationRepository() 

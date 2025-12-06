from flask import Blueprint, render_template
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository
from repositories.notification_repository import NotificationRepository

seller_bp = Blueprint("seller", __name__)

product_repo = ProductRepository()
order_repo = OrderRepository()
notif_repo = NotificationRepository()

SELLER_ID = 3  # مثلاً seller ثابت — عدّلوه بعدين حسب اللوجين

@seller_bp.route("/seller")
def seller_dashboard():
    products = product_repo.get_products_by_seller(SELLER_ID)
    notifications = notif_repo.get_notifications_by_user(SELLER_ID)
    return render_template("seller/dashboard_seller.html",
                           products=products,
                           notifications=notifications)

@seller_bp.route("/seller/products")
def seller_products():
    products = product_repo.get_products_by_seller(SELLER_ID)
    return render_template("seller/seller_products.html", products=products)

@seller_bp.route("/seller/orders")
def seller_orders():
    orders = order_repo.get_orders_for_seller(SELLER_ID)
    return render_template("seller/seller_orders.html", orders=orders)

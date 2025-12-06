from flask import Blueprint, render_template, session, redirect
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository
from repositories.notification_repository import NotificationRepository

seller_bp = Blueprint("seller", __name__)
product_repo = ProductRepository()
order_repo = OrderRepository()
notif_repo = NotificationRepository()
def require_seller():
    if not session.get("user_id") or session.get("role") != "seller":
        return False
    return True
@seller_bp.route("/seller")
def seller_dashboard():
    if not require_seller():
        return redirect("/login")

    seller_id = session["user_id"]
    products = product_repo.get_products_by_seller(seller_id)
    notifications = notif_repo.get_notifications_by_user(seller_id)

    return render_template("seller/dashboard_seller.html",
                           products=products,
                           notifications=notifications)

@seller_bp.route("/seller/products")
def seller_products():
    if not require_seller():
        return redirect("/login")

    seller_id = session["user_id"]
    products = product_repo.get_products_by_seller(seller_id)

    return render_template("seller/seller_products.html",
                           products=products)

@seller_bp.route("/seller/orders")
def seller_orders():
    if not require_seller():
        return redirect("/login")

    seller_id = session["user_id"]
    orders = order_repo.get_orders_for_seller(seller_id)

    return render_template("seller/seller_orders.html",
                           orders=orders)

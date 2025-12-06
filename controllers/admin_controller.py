from flask import Blueprint, render_template
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository

admin_bp = Blueprint("admin", __name__)

user_repo = UserRepository()
product_repo = ProductRepository()

@admin_bp.route("/admin")
def admin_dashboard():
    users = user_repo.get_all()
    products = product_repo.get_all()
    return render_template("admin/admin_dashboard.html", users=users, products=products)

@admin_bp.route("/admin/verify_sellers")
def verify_sellers():
    sellers = [u for u in user_repo.get_all() if u.role == "seller"]
    return render_template("admin/verify_sellers.html", sellers=sellers)

@admin_bp.route("/admin/verify_products")
def verify_products():
    products = product_repo.get_all()
    return render_template("admin/verify_products.html", products=products)

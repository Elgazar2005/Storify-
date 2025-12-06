from flask import Blueprint, render_template, session, redirect
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository

admin_bp = Blueprint("admin", __name__)

user_repo = UserRepository()
product_repo = ProductRepository()


def require_admin():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/login")
    return None


@admin_bp.route("/admin")
def admin_dashboard():
    auth = require_admin()
    if auth:
        return auth

    users = user_repo.get_all()
    products = product_repo.get_all()
    return render_template("admin/admin_dashboard.html", users=users, products=products)


@admin_bp.route("/admin/verify_sellers")
def verify_sellers():
    auth = require_admin()
    if auth:
        return auth

    sellers = [u for u in user_repo.get_all() if u.role == "seller"]
    return render_template("admin/verify_sellers.html", sellers=sellers)


@admin_bp.route("/admin/verify_products")
def verify_products():
    auth = require_admin()
    if auth:
        return auth

    products = product_repo.get_all()
    return render_template("admin/verify_products.html", products=products)
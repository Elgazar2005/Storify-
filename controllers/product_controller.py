from flask import Blueprint, render_template, abort
from repositories.product_repository import ProductRepository

product_bp = Blueprint("product", __name__)
product_repo = ProductRepository()


@product_bp.route("/products")
def list_products():
    products = product_repo.get_all()
    return render_template("products.html", products=products)
 

@product_bp.route("/products/<int:product_id>")
def product_details(product_id):
    product = product_repo.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template("product_details.html", product=product)

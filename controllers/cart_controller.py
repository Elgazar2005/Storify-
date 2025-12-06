from flask import Blueprint, render_template, redirect, url_for, request
from repositories.cart_repository import CartRepository

cart_bp = Blueprint("cart", __name__)
cart_repo = CartRepository()


def get_current_user_id():
    return 1


@cart_bp.route("/cart")
def view_cart():
    user_id = get_current_user_id()
    cart, items_with_products = cart_repo.get_cart_with_products(user_id)
    return render_template(
        "cart.html",
        cart=cart,
        items=items_with_products,
    )


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST", "GET"])
def add_to_cart(product_id):
    user_id = get_current_user_id()
    quantity = request.form.get("quantity", 1)
    cart_repo.add_to_cart(user_id=user_id, product_id=product_id, quantity=int(quantity))
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/cart/remove/<int:product_id>", methods=["POST", "GET"])
def remove_from_cart(product_id):
    user_id = get_current_user_id()
    cart_repo.remove_from_cart(user_id=user_id, product_id=product_id)
    return redirect(url_for("cart.view_cart"))

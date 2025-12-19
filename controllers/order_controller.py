from flask import Blueprint, render_template
from repositories.repository_factory import RepositoryFactory

order_bp = Blueprint("order", __name__)
order_repo = RepositoryFactory.get_order()

@order_bp.route("/orders")
def orders_list():
    orders = order_repo.get_all_orders()
    return render_template("orders.html", orders=orders)

@order_bp.route("/orders/<int:order_id>")
def order_details(order_id):
    order = order_repo.get_order_by_id(order_id)
    if not order:
        return "Order not found", 404
    items = order_repo.get_items_by_order(order_id)
    return render_template("order_details.html", order=order, items=items)

import csv
from Models.order import Order
from Models.orderitem import OrderItem
from repositories.notification_repository import NotificationRepository
from core.file_singletone import FileSingleton

ORDERS_FILE = "orders.csv"
ORDER_ITEMS_FILE = "order_items.csv"
class OrderRepository:
    file = FileSingleton()  # singleton connection
    @staticmethod
    def get_all_orders():
        rows = OrderRepository.file.read_csv(ORDERS_FILE)
        orders = []

        for row in rows:
            orders.append(Order(
                order_id=row["order_id"],
                customer_id=row["customer_id"],
                created_at=row["created_at"],
                status=row["status"],
                total_amount=row["total_amount"]
            ))

        return orders
    @staticmethod
    def add_order(order):
        fieldnames = [
            "order_id",
            "customer_id",
            "created_at",
            "status",
            "total_amount"
        ]

        OrderRepository.file.append_csv(
            ORDERS_FILE,
            fieldnames,
            {
                "order_id": order.order_id,
                "customer_id": order.customer_id,
                "created_at": order.created_at,
                "status": order.status,
                "total_amount": order.total_amount
            }
        )
    @staticmethod
    def get_all_order_items():
        rows = OrderRepository.file.read_csv(ORDER_ITEMS_FILE)
        items = []

        for row in rows:
            items.append(OrderItem(
                order_item_id=row["order_item_id"],
                order_id=row["order_id"],
                product_id=row["product_id"],
                product_name=row["product_name"],
                quantity=int(row["quantity"]),
                price=float(row["price"]),
                seller_id=row["seller_id"]
            ))

        return items
    @staticmethod
    def add_order_item(item):
        fieldnames = [
            "order_item_id",
            "order_id",
            "product_id",
            "product_name",
            "quantity",
            "price",
            "seller_id"
        ]

        OrderRepository.file.append_csv(
            ORDER_ITEMS_FILE,
            fieldnames,
            {
                "order_item_id": item.order_item_id,
                "order_id": item.order_id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "price": item.price,
                "seller_id": item.seller_id
            }
        )
    @staticmethod
    def update_order_item_quantity(order_item_id, new_quantity):
        items = OrderRepository.get_all_order_items()
        updated = False

        for item in items:
            if str(item.order_item_id) == str(order_item_id):
                item.quantity = new_quantity
                updated = True

                if new_quantity < 3:
                    NotificationRepository.add_notification(
                        user_id=item.seller_id,
                        message=f"Quantity for item {item.product_name} is low!",
                        notif_type="low_stock"
                    )
                break
        if updated:
            fieldnames = ["order_item_id",
                "order_id",
                "product_id",
                "product_name",
                "quantity",
                "price",
                "seller_id"]
            rows = []
            for item in items:
                rows.append({
                    "order_item_id": item.order_item_id,
                    "order_id": item.order_id,
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "seller_id": item.seller_id
                })
            OrderRepository.file.write_csv(
                ORDER_ITEMS_FILE,
                fieldnames,
                rows
            )
        return updated
    @staticmethod
    def update_order_status(order_id, new_status):
        orders = OrderRepository.get_all_orders()
        updated = False
        for order in orders:
            if str(order.order_id) == str(order_id):
                order.status = new_status
                updated = True
                break
        if updated:
            fieldnames = ["order_id","customer_id","created_at","status","total_amount"]
            rows = []
            for order in orders:
                rows.append({
                    "order_id": order.order_id,
                    "customer_id": order.customer_id,
                    "created_at": order.created_at,
                    "status": order.status,
                    "total_amount": order.total_amount
                })
            OrderRepository.file.write_csv(ORDERS_FILE,fieldnames,rows)
        return updated

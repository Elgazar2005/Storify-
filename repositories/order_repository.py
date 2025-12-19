import csv
from Models.order import Order
from Models.orderitem import OrderItem
from repositories.notification_repository import NotificationRepository
from core.file_singletone import FileSingleton
from datetime import datetime

ORDERS_FILE = "orders.csv"
ORDER_ITEMS_FILE = "order_items.csv"

class OrderRepository:
    file = FileSingleton() #make object from singltone to make one connection with database

    @staticmethod
    def get_all_orders():
        rows = OrderRepository.file.read_csv(ORDERS_FILE) # read the file by using thefunction from singleton
        orders = [] #make list empty to store data as dictinary to see ass json file
        for row in rows: # make loop to see get each row
            orders.append(Order(
                order_id=row["order_id"],
                customer_id=row["customer_id"],
                created_at=row["created_at"],
                status=row["status"],
                total_amount=row["total_amount"]
            ))
        return orders

    @staticmethod
    def add_order(order): #function to add new order 
        fieldnames = ["order_id", "customer_id", "created_at", "status", "total_amount"]

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
        fieldnames = ["order_item_id", "order_id", "product_id",
                      "product_name", "quantity", "price", "seller_id"]

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
            if item.order_item_id == order_item_id:
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
            fieldnames = ["order_item_id", "order_id", "product_id",
                          "product_name", "quantity", "price", "seller_id"]

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

            OrderRepository.file.write_csv(ORDER_ITEMS_FILE, fieldnames, rows)

        return updated

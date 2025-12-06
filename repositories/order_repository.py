import csv #library that use to read CSV file
from Models.order import Order #import file model
from Models.orderitem import OrderItem #import file model
from repositories.notification_repository import NotificationRepository #to add notification to seller 
from datetime import datetime # to get live time

# make varibles to path 
ORDERS_FILE = "orders.csv"
ORDER_ITEMS_FILE = "order_items.csv"

class OrderRepository:
    @staticmethod #that function is work without need to make object of class
    def get_all_orders(): 
        orders = [] #make the list of Orders
        with open(ORDERS_FILE, newline="", encoding="utf-8") as csvfile: #open file CSV with UTF-8 at mode Read
            reader = csv.DictReader(csvfile) #change file to dictonary and make header for each column is key
            for row in reader: #loop on each row in dictonary
                # Create an Order object from the current CSV row
                # Each column in the CSV row is mapped to an attribute of the Order object
                order = Order( 
                    order_id=row["order_id"],
                    customer_id=row["customer_id"],
                    created_at=row["created_at"],
                    status=row["status"],
                    total_amount=row["total_amount"]
                )
                orders.append(order) # add this object to list of orders
        return orders #return list of orders to use it 

    @staticmethod #that function is work without need to make object of class
    # Add a new Order object to the CSV file
    # The parameter 'order' should be an Order object
    def add_order(order):
        with open(ORDERS_FILE, "a", newline="", encoding="utf-8") as csvfile: #Open file in mode write and "a" that mean append that write to file without remove the old dara
            writer = csv.writer(csvfile)
            # Write order of headers of Csv file to write under it like refrance to us
            writer.writerow([order.order_id, order.customer_id, order.created_at, order.status, order.total_amount])

    @staticmethod #that function is work without need to make object of class
    def get_all_order_items(): # make function to read from order_item to store it
        items = [] # make empty list to put item in it 
        with open(ORDER_ITEMS_FILE, newline="", encoding="utf-8") as csvfile: # open file with remove any space in beginning
            reader = csv.DictReader(csvfile) #change file to dictonary and make header for each column is key
            for row in reader: #loop on each row in dictonary
                # Create an item object from the current CSV row
                # Each column in the CSV row is mapped to an attribute of the Item object
                item = OrderItem(
                    order_item_id=row["order_item_id"],
                    order_id=row["order_id"],
                    product_id=row["product_id"],
                    product_name=row["product_name"],
                    quantity=int(row["quantity"]),
                    price=float(row["price"]),
                    seller_id=row["seller_id"]
                )
                items.append(item) # add this object to list of items
        return items #return list of orders to use it 

    @staticmethod
    # Add a new Order object to the CSV file
    # The parameter 'order' should be an Order object
    def add_order_item(item):
        with open(ORDER_ITEMS_FILE, "a", newline="", encoding="utf-8") as csvfile: #Open file in mode write and "a" that mean append that write to file without remove the old dara
            writer = csv.writer(csvfile)
            # Write order of headers of Csv file to write under it like refrance to us
            writer.writerow([item.order_item_id, item.order_id, item.product_id, item.product_name, item.quantity, item.price,item.seller_id])

    @staticmethod
    def update_order_item_quantity(order_item_id, new_quantity): #function that take new quantity of item that we gt by id
        items = OrderRepository.get_all_order_items() # get all item by function
        updated = False #boolen variable is initail equal false
        for item in items:
            if item.order_item_id == order_item_id: #search for an item id that we want to chane it stock
                item.quantity = new_quantity # if we get it we update the quantity
                updated = True
                seller_id = item.seller_id
                if new_quantity < 3: #if we add quantity less than 3 we sent alert to seller
                    NotificationRepository.add_notification(
                        user_id=seller_id,
                        message=f"Quantity for item {item.product_name} is low!",
                        type="low_stock"
                    )
        if updated:
            with open(ORDER_ITEMS_FILE, "w", newline="", encoding="utf-8") as csvfile: #open file in mode W that delete all data and write new
                writer = csv.writer(csvfile)
                writer.writerow(["order_item_id","order_id","product_id","product_name","quantity","price","seller_id"])
                for item in items:
                    writer.writerow([item.order_item_id,item.order_id,item.product_id,item.product_name,item.quantity,item.price,item.seller_id])

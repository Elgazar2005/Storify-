import csv
from Models.cart import Cart, CartItem
from Models.product import Product
from repositories.product_repository import ProductRepository


class CartRepository:
    def __init__(
        self,
        carts_file_path="data/carts.csv",
        cart_items_file_path="data/cart_items.csv",
    ):
        self.carts_file_path = carts_file_path
        self.cart_items_file_path = cart_items_file_path
        self.product_repo = ProductRepository()


    def _read_carts(self):
        carts = []
        with open(self.carts_file_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                carts.append(Cart(
                    id=row["id"],
                    user_id=row["user_id"],
                    status=row["status"],
                ))
        return carts

    def _read_cart_items(self):
        items = []
        with open(self.cart_items_file_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(CartItem(
                    id=row["id"],
                    cart_id=row["cart_id"],
                    product_id=row["product_id"],
                    quantity=row["quantity"],
                ))
        return items

    def _write_cart_items(self, cart_items):
        fieldnames = ["id", "cart_id", "product_id", "quantity"]
        with open(self.cart_items_file_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in cart_items:
                writer.writerow({
                    "id": item.id,
                    "cart_id": item.cart_id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                })


    def get_open_cart_for_user(self, user_id: int):
        for cart in self._read_carts():
            if cart.user_id == int(user_id) and cart.status == "open":
                return cart
        return None

    def get_items_for_cart(self, cart_id: int):
        return [item for item in self._read_cart_items() if item.cart_id == int(cart_id)]

    def get_cart_with_products(self, user_id: int):
        """
        Return tuple: (cart, items_with_products)
        items_with_products = list of dict {item, product}
        """
        cart = self.get_open_cart_for_user(user_id)
        if not cart:
            return None, []

        items = self.get_items_for_cart(cart.id)
        result = []
        for item in items:
            product = self.product_repo.get_by_id(item.product_id)
            result.append({
                "item": item,
                "product": product,
            })
        return cart, result

    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1):
        cart = self.get_open_cart_for_user(user_id)
        if not cart:
            carts = self._read_carts()
            new_id = max([c.id for c in carts], default=0) + 1
            cart = Cart(id=new_id, user_id=user_id, status="open")
            carts.append(cart)

            fieldnames = ["id", "user_id", "status"]
            with open(self.carts_file_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for c in carts:
                    writer.writerow({
                        "id": c.id,
                        "user_id": c.user_id,
                        "status": c.status,
                    })

        cart_items = self._read_cart_items()
        for item in cart_items:
            if item.cart_id == cart.id and item.product_id == int(product_id):
                item.quantity += int(quantity)
                self._write_cart_items(cart_items)
                return

        new_id = max([ci.id for ci in cart_items], default=0) + 1
        cart_items.append(CartItem(
            id=new_id,
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
        ))
        self._write_cart_items(cart_items)

    def remove_from_cart(self, user_id: int, product_id: int):
        cart = self.get_open_cart_for_user(user_id)
        if not cart:
            return

        cart_items = self._read_cart_items()
        filtered = [
            item for item in cart_items
            if not (item.cart_id == cart.id and item.product_id == int(product_id))
        ]
        self._write_cart_items(filtered)

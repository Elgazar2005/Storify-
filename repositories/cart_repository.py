from Models.cart import Cart
from Models.cartitem import CartItem
from repositories.product_repository import ProductRepository
from core.file_singletone import FileSingleton


class CartRepository:
    def __init__(self,
                 carts_file_path="data/carts.csv",
                 cart_items_file_path="data/cart_items.csv"):
        self.carts_file_path = carts_file_path
        self.cart_items_file_path = cart_items_file_path
        self.product_repo = ProductRepository()
        self.file = FileSingleton()

    def _read_carts(self):
        rows = self.file.read_csv(self.carts_file_path)
        return [Cart(
            id=int(r["id"]),
            user_id=int(r["user_id"]),
            status=r["status"]
        ) for r in rows]

    def _read_cart_items(self):
        rows = self.file.read_csv(self.cart_items_file_path)
        return [CartItem(
            id=int(r["id"]),
            cart_id=int(r["cart_id"]),
            product_id=int(r["product_id"]),
            quantity=int(r["quantity"])
        ) for r in rows]

    def _write_cart_items(self, items):
        rows = [{
            "id": i.id,
            "cart_id": i.cart_id,
            "product_id": i.product_id,
            "quantity": i.quantity
        } for i in items]

        self.file.write_csv(
            self.cart_items_file_path,
            ["id", "cart_id", "product_id", "quantity"],
            rows
        )

    def _write_carts(self, carts):
        rows = [{
            "id": c.id,
            "user_id": c.user_id,
            "status": c.status
        } for c in carts]

        self.file.write_csv(
            self.carts_file_path,
            ["id", "user_id", "status"],
            rows
        )

    def get_open_cart_for_user(self, user_id):
        for cart in self._read_carts():
            if cart.user_id == user_id and cart.status == "open":
                return cart
        return None

    def get_cart_with_products(self, user_id):
        cart = self.get_open_cart_for_user(user_id)
        if not cart:
            return None, []

        items = self._read_cart_items()
        result = []

        for item in items:
            if item.cart_id == cart.id:
                product = self.product_repo.get_by_id(item.product_id)
                result.append({
                    "item": item,
                    "product": product
                })

        return cart, result

    def add_to_cart(self, user_id, product_id, quantity=1):
        carts = self._read_carts()
        cart = self.get_open_cart_for_user(user_id)

        if not cart:
            new_id = max([c.id for c in carts], default=0) + 1
            cart = Cart(new_id, user_id, "open")
            carts.append(cart)
            self._write_carts(carts)

        items = self._read_cart_items()
        for item in items:
            if item.cart_id == cart.id and item.product_id == product_id:
                item.quantity += quantity
                self._write_cart_items(items)
                return

        new_id = max([i.id for i in items], default=0) + 1
        items.append(CartItem(new_id, cart.id, product_id, quantity))
        self._write_cart_items(items)

    def remove_from_cart(self, user_id, product_id):
        cart = self.get_open_cart_for_user(user_id)
        if not cart:
            return

        items = self._read_cart_items()
        items = [
            i for i in items
            if not (i.cart_id == cart.id and i.product_id == product_id)
        ]
        self._write_cart_items(items)

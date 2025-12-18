from Models.product import Product
from core.file_singletone import FileSingleton


class ProductRepository:
    def __init__(self, products_file_path="data/products.csv"):
        self.products_file_path = products_file_path
        self.file = FileSingleton()

    def get_all(self):
        rows = self.file.read_csv(self.products_file_path)
        products = []

        for row in rows:
            products.append(Product(
                id=int(row["id"]),
                name=row["name"],
                description=row["description"],
                price=float(row["price"]),   # مهم
                stock=int(row["stock"]),
                image=row["image"]
            ))
        return products

    def get_by_id(self, product_id: int):
        for product in self.get_all():
            if product.id == int(product_id):
                return product
        return None



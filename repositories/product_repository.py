import csv
from Models.product import Product

class ProductRepository:
    def __init__(self, products_file_path="data/products.csv"):
        self.products_file_path = products_file_path

    def _read_all_rows(self):
        products = []
        with open(self.products_file_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                products.append(Product(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    price=row["price"],
                    stock=row["stock"],
                ))
        return products

    def get_all(self):
        """Return list of Product objects"""
        return self._read_all_rows()

    def get_by_id(self, product_id: int):
        for product in self._read_all_rows():
            if product.id == int(product_id):
                return product
        return None
# تم بحمدالله
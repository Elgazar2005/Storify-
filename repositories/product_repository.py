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
                    image=row["image"]    # مهم جداً
                ))
        return products

    def _write_all_rows(self, products):
        with open(self.products_file_path, "w", newline='', encoding="utf-8") as f:
            fieldnames = ["id", "name", "description", "price", "stock", "image"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for p in products:
                writer.writerow({
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "price": p.price,
                    "stock": p.stock,
                    "image": p.image
                })

    def get_all(self):
        return self._read_all_rows()

    def get_by_id(self, product_id: int):
        for product in self._read_all_rows():
            if product.id == int(product_id):
                return product
        return None

    def add(self, product: Product):
        products = self._read_all_rows()
        if any(p.id == product.id for p in products):
            raise ValueError("Product with this ID already exists")

        products.append(product)
        self._write_all_rows(products)

    def update(self, product: Product):
        products = self._read_all_rows()
        for i, p in enumerate(products):
            if p.id == product.id:
                products[i] = product
                self._write_all_rows(products)
                return True
        return False

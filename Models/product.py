class Product:
    def __init__(self, id, name, description, price, stock, image):
        self.id = int(id)
        self.name = name
        self.description = description
        self.price = float(price)
        self.stock = int(stock)
        self.image = image   

    def __repr__(self):
        return f"<Product {self.id} - {self.name}>"

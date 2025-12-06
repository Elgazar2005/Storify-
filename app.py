from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# -------------------------
#      PUBLIC ROUTES
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # handle login
        pass
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # handle signup
        pass
    return render_template("signup.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/product/<product_id>")
def product_details(product_id):
    return render_template("product_details.html", product_id=product_id)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/orders")
def orders():
    return render_template("orders.html")


# -------------------------
#     SELLER ROUTES
# -------------------------

@app.route("/seller/dashboard")
def seller_dashboard():
    return render_template("seller/dashboard_seller.html")

@app.route("/seller/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        # handle add product
        pass
    return render_template("seller/add_product.html")

# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)

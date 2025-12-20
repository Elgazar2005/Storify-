from flask import Flask, render_template, request, redirect, url_for, session, abort
import csv, os, datetime

app = Flask(__name__)
app.secret_key = "storify_csv_secret"

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

USERS_CSV = os.path.join(DATA_DIR, "users.csv")
PRODUCTS_CSV = os.path.join(DATA_DIR, "products.csv")
CARTS_CSV = os.path.join(DATA_DIR, "carts.csv")
CART_ITEMS_CSV = os.path.join(DATA_DIR, "cart_items.csv")
ORDERS_CSV = os.path.join(DATA_DIR, "orders.csv")
ORDER_ITEMS_CSV = os.path.join(DATA_DIR, "order_items.csv")
NOTIFICATIONS_CSV = os.path.join(DATA_DIR, "notifications.csv")
VERIFICATION_REQ_CSV = os.path.join(DATA_DIR, "verification_requests.csv")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def read_csv(path):
    ensure_data_dir()
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(path, rows, fieldnames):
    ensure_data_dir()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def append_csv(path, row, fieldnames):
    ensure_data_dir()
    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def next_id(rows, id_field="id"):
    if not rows:
        return 1
    try:
        return max(int(r[id_field]) for r in rows if r.get(id_field)) + 1
    except Exception:
        return len(rows) + 1

def ensure_csv_headers():
    ensure_data_dir()
    if not os.path.exists(USERS_CSV):
        write_csv(USERS_CSV, [], ["id","username","email","password","role"])
    if not os.path.exists(PRODUCTS_CSV):
        write_csv(PRODUCTS_CSV, [], ["id","name","description","price","stock"])
    if not os.path.exists(CARTS_CSV):
        write_csv(CARTS_CSV, [], ["id","user_id","status"])
    if not os.path.exists(CART_ITEMS_CSV):
        write_csv(CART_ITEMS_CSV, [], ["id","cart_id","product_id","quantity"])
    if not os.path.exists(ORDERS_CSV):
        write_csv(ORDERS_CSV, [], ["order_id","customer_id","created_at","status","total_amount"])
    if not os.path.exists(ORDER_ITEMS_CSV):
        write_csv(ORDER_ITEMS_CSV, [], ["order_item_id","order_id","product_id","product_name","quantity","price","seller_id"])
    if not os.path.exists(NOTIFICATIONS_CSV):
        write_csv(NOTIFICATIONS_CSV, [], ["notification_id","user_id","message","type","is_read","created_at"])
    if not os.path.exists(VERIFICATION_REQ_CSV):
        write_csv(VERIFICATION_REQ_CSV, [], ["id","username","email","reason","created_at"])

ensure_csv_headers()

def get_all_users():
    return read_csv(USERS_CSV)

def get_user_by_id(uid):
    for u in get_all_users():
        if str(u.get("id")) == str(uid):
            return u
    return None

def get_user_by_email_password(email, password):
    for u in get_all_users():
        if u.get("email") == email and u.get("password") == password:
            return u
    return None

def create_user(username, email, password, role="customer"):
    users = read_csv(USERS_CSV)
    uid = next_id(users, id_field="id")
    row = {"id": str(uid), "username": username, "email": email, "password": password, "role": role}
    append_csv(USERS_CSV, row, ["id","username","email","password","role"])
    return row

def get_all_products():
    rows = read_csv(PRODUCTS_CSV)
    for r in rows:
        r["price"] = float(r.get("price", 0)) if r.get("price","")!="" else 0.0
        r["stock"] = int(float(r.get("stock", 0))) if r.get("stock","")!="" else 0
    return rows

def get_product_by_id(pid):
    for p in get_all_products():
        if str(p.get("id")) == str(pid):
            return p
    return None

def create_product(name, description, price, stock=0, seller_id=""):
    rows = read_csv(PRODUCTS_CSV)
    pid = next_id(rows, id_field="id")
    row = {"id": str(pid), "name": name, "description": description, "price": str(price), "stock": str(stock)}
    append_csv(PRODUCTS_CSV, row, ["id","name","description","price","stock"])
    return row

def update_product(pid, **fields):
    rows = read_csv(PRODUCTS_CSV)
    changed = False
    for r in rows:
        if str(r.get("id")) == str(pid):
            for k,v in fields.items():
                if k in r:
                    r[k] = str(v)
            changed = True
            break
    if changed:
        fieldnames = ["id","name","description","price","stock"]
        write_csv(PRODUCTS_CSV, rows, fieldnames)
    return changed

def get_all_orders():
    return read_csv(ORDERS_CSV)

def get_order_by_id(oid):
    for o in get_all_orders():
        if str(o.get("order_id")) == str(oid):
            return o
    return None

def get_order_items(order_id):
    items = read_csv(ORDER_ITEMS_CSV)
    return [i for i in items if str(i.get("order_id")) == str(order_id)]

def create_order(customer_id, total_amount, items):
    orders = read_csv(ORDERS_CSV)
    oid = next_id(orders, id_field="order_id")
    created_at = datetime.datetime.utcnow().isoformat()
    order_row = {"order_id": str(oid), "customer_id": str(customer_id), "created_at": created_at, "status":"pending", "total_amount": str(total_amount)}
    append_csv(ORDERS_CSV, order_row, ["order_id","customer_id","created_at","status","total_amount"])
    oi = read_csv(ORDER_ITEMS_CSV)
    next_item_id = next_id(oi, id_field="order_item_id")
    for it in items:
        item_row = {
            "order_item_id": str(next_item_id),
            "order_id": str(oid),
            "product_id": str(it["product_id"]),
            "product_name": it["product_name"],
            "quantity": str(it["quantity"]),
            "price": str(it["price"]),
            "seller_id": str(it.get("seller_id",""))
        }
        append_csv(ORDER_ITEMS_CSV, item_row, ["order_item_id","order_id","product_id","product_name","quantity","price","seller_id"])
        next_item_id += 1
    return order_row

def get_notifications_for_user(user_id):
    nots = read_csv(NOTIFICATIONS_CSV)
    return [n for n in nots if str(n.get("user_id")) == str(user_id)]

def get_session_cart():
    if "cart" not in session:
        session["cart"] = []
    return session["cart"]

def add_to_session_cart(product_id, qty):
    cart = get_session_cart()
    for it in cart:
        if str(it["product_id"]) == str(product_id):
            it["quantity"] = int(it["quantity"]) + int(qty)
            session.modified = True
            return
    cart.append({"product_id": str(product_id), "quantity": int(qty)})
    session.modified = True

def remove_from_session_cart(product_id):
    cart = get_session_cart()
    session["cart"] = [it for it in cart if str(it["product_id"]) != str(product_id)]
    session.modified = True

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return get_user_by_id(uid)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user_by_email_password(email, password)
    if not user:
        return render_template("login.html", error="Invalid credentials")
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    if user["role"] == "seller":
        return redirect(url_for("seller_dashboard"))
    if user["role"] == "admin":
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    create_user(username, email, password, role="customer")
    u = get_user_by_email_password(email, password)
    session["user_id"] = u["id"]
    session["role"] = u["role"]
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/products")
def list_products():
    products = get_all_products()
    return render_template("products.html", products=products)

@app.route("/products/<int:product_id>", methods=["GET","POST"])
def product_details(product_id):
    p = get_product_by_id(product_id)
    if not p:
        abort(404)
    if request.method == "POST":
        qty = int(request.form.get("quantity", 1))
        add_to_session_cart(product_id, qty)
        return redirect(url_for("cart"))
    return render_template("product_details.html", product=p)

@app.route("/cart")
def cart():
    cart_items = get_session_cart()
    items_with_products = []
    total_price = 0.0

    for it in cart_items:
        prod = get_product_by_id(it["product_id"])
        if prod:
            subtotal = float(prod["price"]) * int(it["quantity"])
            total_price += subtotal
            items_with_products.append({
                "item": it,
                "product": prod
            })

    return render_template(
        "cart.html",
        cart=cart_items,
        items=items_with_products,
        total_price=total_price
    )


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    qty = int(request.form.get("quantity", 1))
    add_to_session_cart(product_id, qty)
    return redirect(url_for("cart"))

@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    remove_from_session_cart(product_id)
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET","POST"])
def checkout():
    cart_items = get_session_cart()
    items_list = []
    total = 0.0
    for it in cart_items:
        prod = get_product_by_id(it["product_id"])
        if not prod:
            continue
        items_list.append({"product_id": prod["id"], "product_name": prod["name"], "quantity": int(it["quantity"]), "price": float(prod["price"])})
        total += float(prod["price"]) * int(it["quantity"])
    if request.method == "POST":
        user = current_user()
        customer_id = user["id"] if user else "guest"
        order = create_order(customer_id, total, items_list)
        session["cart"] = []
        return redirect(url_for("orders_list"))
    return render_template("checkout.html", items=items_list, total=total)

@app.route("/orders")
def orders_list():
    orders = get_all_orders()
    return render_template("orders.html", orders=orders)

@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    order = get_order_by_id(order_id)
    if not order:
        abort(404)
    items = get_order_items(order_id)
    return render_template("order_details.html", order=order, items=items)

@app.route("/seller")
def seller_dashboard():
    if not session.get("user_id") or session.get("role") != "seller":
        return redirect(url_for("login"))
    seller_id = session.get("user_id")
    prods = get_all_products()
    seller_products = [p for p in prods if str(p.get("seller_id","")) == str(seller_id) or p.get("seller_id","")==""]
    notifications = get_notifications_for_user(seller_id)
    return render_template("seller/dashboard_seller.html", products=seller_products, notifications=notifications)

@app.route("/seller/products")
def my_products():
    if not session.get("user_id") or session.get("role") != "seller":
        return redirect(url_for("login"))
    seller_id = session.get("user_id")
    prods = get_all_products()
    seller_products = [p for p in prods if str(p.get("seller_id","")) == str(seller_id) or p.get("seller_id","")==""]
    return render_template("seller/seller_products.html", products=seller_products)

@app.route("/seller/add_product", methods=["GET","POST"])
def add_product():
    if not session.get("user_id") or session.get("role") != "seller":
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        seller_id = session.get("user_id")
        create_product(name, description, price, stock=10, seller_id=seller_id)
        return redirect(url_for("seller_dashboard"))
    return render_template("seller/add_product.html")

@app.route("/seller/products/<int:product_id>/edit", methods=["GET","POST"])
def edit_product(product_id):
    if not session.get("user_id") or session.get("role") != "seller":
        return redirect(url_for("login"))
    prod = get_product_by_id(product_id)
    if not prod:
        abort(404)
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        update_product(product_id, name=name, price=price, stock=stock)
        return redirect(url_for("my_products"))
    return render_template("seller/edit_product.html", product=prod)

@app.route("/seller/orders")
def seller_orders():
    if not session.get("user_id") or session.get("role") != "seller":
        return redirect(url_for("login"))
    seller_id = session.get("user_id")
    orders = get_all_orders()
    matching = []
    for o in orders:
        items = get_order_items(o.get("order_id"))
        for it in items:
            prod = get_product_by_id(it.get("product_id"))
            if prod and str(prod.get("seller_id","")) == str(seller_id):
                matching.append(o)
                break
    return render_template("seller/seller_orders.html", orders=matching)

@app.route("/admin")
def admin_dashboard():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect(url_for("login"))
    users = get_all_users()
    products = get_all_products()
    return render_template("admin/admin_dashboard.html", users=users, products=products)

@app.route("/admin/verify_sellers")
def admin_verify_sellers():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect(url_for("login"))
    sellers = [u for u in get_all_users() if u.get("role") == "seller"]
    return render_template("admin/verify_sellers.html", sellers=sellers)

@app.route("/admin/verify_products")
def admin_verify_products():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect(url_for("login"))
    products = get_all_products()
    return render_template("admin/verify_products.html", products=products)

@app.route("/users")
def users_list():
    users = get_all_users()
    return render_template("user/list.html", users=users)

@app.route("/users/<int:user_id>")
def user_profile(user_id):
    u = get_user_by_id(user_id)
    if not u:
        abort(404)
    return render_template("user/profile.html", user=u)

app.add_url_rule("/products", endpoint="product.list_products", view_func=list_products)
app.add_url_rule("/products/<int:product_id>", endpoint="product.product_details", view_func=product_details)
app.add_url_rule("/cart/add/<int:product_id>", endpoint="cart.add_to_cart", view_func=add_to_cart, methods=["POST"])
app.add_url_rule("/cart/remove/<int:product_id>", endpoint="cart.remove_from_cart", view_func=remove_from_cart, methods=["POST"])
app.add_url_rule("/seller/products", endpoint="my_products", view_func=my_products)
app.add_url_rule("/seller/products/<int:product_id>/edit", endpoint="edit_product", view_func=edit_product, methods=["GET","POST"])
app.add_url_rule("/seller/orders", endpoint="seller_orders", view_func=seller_orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

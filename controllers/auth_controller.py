from flask import Blueprint, render_template, request, redirect, session
from repositories.user_repository import UserRepository
from repositories.repository_factory import RepositoryFactory

auth_bp = Blueprint("auth", __name__)
user_repo = RepositoryFactory.get_user()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    users = user_repo.get_all()

    for user in users:
        if user.email == email and user.password == password:
            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "seller":
                return redirect("/seller")
            elif user.role == "admin":
                return redirect("/admin")
            else:
                return redirect(f"/users/{user.id}")

    return "Invalid email or password", 401


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    role = "customer"

    user_repo.create_user(username=username, email=email, password=password, role=role)

    users = user_repo.get_all()
    new_user = users[-1]

    session["user_id"] = new_user.id
    session["role"] = new_user.role

    return redirect(f"/users/{new_user.id}")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
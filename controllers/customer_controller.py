from flask import Blueprint, render_template, request, redirect, url_for
from repositories.user_repository import UserRepository

user_bp = Blueprint("user", __name__)
user_repo = UserRepository()


@user_bp.route("/users")
def users_list():
    all_users = user_repo.get_all()
    return render_template("user/list.html", users=all_users)


@user_bp.route("/users/<int:user_id>")
def user_profile(user_id):
    user = user_repo.get_by_id(user_id)
    if not user:
        return "User not found", 404
    return render_template("user/profile.html", user=user)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    for user in user_repo.get_all():
        if user.email == email and user.password == password:
            return redirect(f"/users/{user.id}")

    return "Invalid email or password", 401


@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    return f"Signup logic pending for: {username}", 200

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("films.home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        errors = []
        if len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        if len(password) < 4:
            errors.append("Password must be at least 4 characters.")
        if User.query.filter_by(username=username).first():
            errors.append("This username is already taken.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("register.html", username=username)

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Welcome! Your account has been created. 🎉", "success")
        return redirect(url_for("films.home"))
    return render_template("register.html", username="")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("films.home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully! 👋", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("films.home"))
        flash("Invalid username or password.", "danger")
        return render_template("login.html", username=username)
    return render_template("login.html", username="")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("films.home"))

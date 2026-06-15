from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Film

favorites_bp = Blueprint("favorites", __name__)


@favorites_bp.route("/favorite/<int:film_id>", methods=["POST"])
@login_required
def toggle_favorite(film_id):
    film = db.get_or_404(Film, film_id)
    if film in current_user.favorites:
        current_user.favorites.remove(film)
        flash(f"Removed “{film.title}” from favorites.", "info")
    else:
        current_user.favorites.append(film)
        flash(f"Added “{film.title}” to favorites! ❤️", "success")
    db.session.commit()
    return redirect(request.referrer or url_for("films.home"))


@favorites_bp.route("/favorites")
@login_required
def my_favorites():
    return render_template("favorites.html", films=current_user.favorites)

from flask import Blueprint, render_template, request, redirect, url_for, flash

from extensions import db
from models import Film
from validators import validate_film
from decorators import admin_required

films_bp = Blueprint("films", __name__)

PER_PAGE = 24


@films_bp.route("/")
def home():
    q = request.args.get("q", "").strip()
    sort = request.args.get("sort", "rating_desc")
    page = request.args.get("page", 1, type=int)

    stmt = db.select(Film)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(db.or_(Film.title.ilike(like), Film.director.ilike(like)))

    sort_options = {
        "title": Film.title.asc(),
        "year_desc": Film.year.desc(),
        "year_asc": Film.year.asc(),
        "rating_desc": Film.rating.desc(),
        "rating_asc": Film.rating.asc(),
    }
    stmt = stmt.order_by(sort_options.get(sort, Film.rating.desc()))

    pagination = db.paginate(stmt, page=page, per_page=PER_PAGE, error_out=False)
    return render_template("index.html", pagination=pagination,
                           films=pagination.items, q=q, sort=sort)


@films_bp.route("/film/<int:film_id>")
def film_detail(film_id):
    film = db.get_or_404(Film, film_id)
    return render_template("detail.html", film=film)


@films_bp.route("/add", methods=["GET", "POST"])
@admin_required
def add_film():
    if request.method == "POST":
        data, errors = validate_film(request.form)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("form.html", title="Add Movie", film=data)
        film = Film(
            title=data["title"], director=data["director"],
            year=int(data["year"]), rating=float(data["rating"].replace(",", ".")),
            cover=data["cover"], overview=data["overview"],
        )
        db.session.add(film)
        db.session.commit()
        flash("Movie added! 🎬", "success")
        return redirect(url_for("films.home"))
    return render_template("form.html", title="Add Movie", film=None)


@films_bp.route("/edit/<int:film_id>", methods=["GET", "POST"])
@admin_required
def edit_film(film_id):
    film = db.get_or_404(Film, film_id)
    if request.method == "POST":
        data, errors = validate_film(request.form)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("form.html", title="Edit Movie", film=data)
        film.title = data["title"]
        film.director = data["director"]
        film.year = int(data["year"])
        film.rating = float(data["rating"].replace(",", "."))
        film.cover = data["cover"]
        film.overview = data["overview"]
        db.session.commit()
        flash("Changes saved! ✅", "success")
        return redirect(url_for("films.home"))
    return render_template("form.html", title="Edit Movie", film=film)


@films_bp.route("/delete/<int:film_id>", methods=["POST"])
@admin_required
def delete_film(film_id):
    film = db.get_or_404(Film, film_id)
    db.session.delete(film)
    db.session.commit()
    flash("Movie deleted 🗑", "info")
    return redirect(url_for("films.home"))

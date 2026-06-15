def validate_film(form):
    title = form.get("title", "").strip()
    director = form.get("director", "").strip()
    year_raw = form.get("year", "").strip()
    rating_raw = form.get("rating", "").strip()
    cover = form.get("cover", "").strip()
    overview = form.get("overview", "").strip()

    errors = []

    if not title:
        errors.append("Title is required.")
    elif len(title) > 300:
        errors.append("Title is too long (max 300 characters).")

    if not director:
        errors.append("Director is required.")
    elif len(director) > 200:
        errors.append("Director name is too long (max 200 characters).")

    year = None
    if not year_raw:
        errors.append("Year is required.")
    else:
        try:
            year = int(year_raw)
            if year < 1888 or year > 2030:
                errors.append("Year must be between 1888 and 2030.")
        except ValueError:
            errors.append("Year must be a whole number (e.g. 2010).")

    rating = None
    if not rating_raw:
        errors.append("Rating is required.")
    else:
        try:
            rating = float(rating_raw.replace(",", "."))
            if rating < 0 or rating > 10:
                errors.append("Rating must be between 0 and 10.")
        except ValueError:
            errors.append("Rating must be a number (e.g. 8.5).")

    data = {
        "title": title, "director": director, "year": year_raw,
        "rating": rating_raw, "cover": cover, "overview": overview,
    }
    return data, errors

import csv
import json

from app import app
from models import db, Film

csv.field_size_limit(10_000_000)

DATA = r"C:\Users\dropbliin\Downloads\movies-dataset"


directors = {}
with open(DATA + r"\credits.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        try:
            for person in json.loads(row["crew"]):
                if person.get("job") == "Director":
                    directors[row["movie_id"]] = person["name"]
                    break
        except Exception:
            pass

posters = {}
with open(DATA + r"\poster.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        title = row["title"].strip()
        poster = row["poster"].strip()
        if title and poster:
            posters[title] = poster

films = []
with open(DATA + r"\movies.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        title = row["title"].strip()
        cover = posters.get(title)
        if not cover:
            continue

        year = None
        release = row["release_date"].strip()
        if len(release) >= 4 and release[:4].isdigit():
            year = int(release[:4])

        rating = None
        try:
            rating = float(row["vote_average"]) if row["vote_average"] else None
        except ValueError:
            pass

        films.append(Film(
            title=title,
            director=directors.get(row["id"], ""),
            year=year,
            rating=rating,
            cover=cover,
            overview=row["overview"].strip(),
        ))

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.bulk_save_objects(films)
    db.session.commit()
    print("Imported films:", Film.query.count())

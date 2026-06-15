from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


favorites = db.Table(
    "favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("film_id", db.Integer, db.ForeignKey("films.id"), primary_key=True),
)


class Film(db.Model):
    __tablename__ = "films"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    director = db.Column(db.String(200))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    cover = db.Column(db.String(500))
    overview = db.Column(db.Text)

    def __repr__(self):
        return f"<Film {self.title} ({self.year})>"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    favorites = db.relationship("Film", secondary=favorites, backref="fans")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

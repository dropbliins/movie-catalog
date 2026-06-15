import os
from flask import Flask
from dotenv import load_dotenv

from extensions import db, login_manager
from models import User
from controllers.films import films_bp
from controllers.favorites import favorites_bp
from controllers.auth import auth_bp

load_dotenv()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."
    login_manager.login_message_category = "warning"

    app.register_blueprint(films_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", is_admin=True)
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

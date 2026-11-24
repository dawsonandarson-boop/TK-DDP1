"""Pabrik aplikasi Flask dan registrasi route."""
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("moodify.config.Config")

    from moodify.routes.main import main_bp
    app.register_blueprint(main_bp)
    return app

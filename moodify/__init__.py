"""Pabrik aplikasi Flask dan registrasi route."""
from flask import Flask


def create_app():
    # Template dan static berada di root proyek, sejajar dengan app.py.
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/static",
    )
    app.config.from_object("moodify.config.Config")

    from moodify.routes.main import main_bp
    app.register_blueprint(main_bp)
    return app

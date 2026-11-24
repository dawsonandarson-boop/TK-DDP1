"""Route halaman. Hubungkan tiap form dengan service saat fitur dikerjakan."""
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    return render_template("home.html")


@main_bp.get("/search")
def search():
    # TODO: Terima query judul/artis, prompt, atau mood dan panggil search_service.
    return render_template("search_results.html", results=None)


@main_bp.get("/recommend")
def recommend():
    # TODO: Terima curhat, panggil mood_service dan recommendation_service.
    return render_template("recommendations.html", recommendations=None)


@main_bp.get("/catalog")
def catalog():
    # TODO: Ambil/filter lagu dari katalog lokal.
    return render_template("catalog.html", songs=None)


@main_bp.get("/favorites")
def favorites():
    # TODO: Tampilkan favorit berdasarkan sesi browser, tanpa akun.
    return render_template("favorites.html", songs=None)


@main_bp.get("/history")
def history():
    # TODO: Tampilkan riwayat rekomendasi yang terkait sesi browser.
    return render_template("history.html", entries=None)


@main_bp.get("/song/<int:song_id>")
def song_detail(song_id):
    # TODO: Ambil lagu dan siapkan detail, preview, lirik, serta tautan dengar.
    return render_template("song_detail.html", song=None, song_id=song_id)

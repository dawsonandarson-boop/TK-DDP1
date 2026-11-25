"""Route halaman. Tahap ini memakai data contoh, belum memanggil API musik."""
from flask import Blueprint, render_template, request

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    return render_template("home.html")


@main_bp.route("/search", methods=["GET", "POST"])
def search():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        # Data contoh sementara supaya alur form dan halaman hasil bisa dipelajari.
        # Tahap berikutnya, data ini akan diganti hasil dari Deezer/iTunes.
        demo_songs = [
            {"title": "Dekat di Hati", "artist": "RAN", "album": "Hari Baru"},
            {"title": "Evaluasi", "artist": "Hindia", "album": "Menari Dengan Bayangan"},
            {"title": "Sorai", "artist": "Nadin Amizah", "album": "Selamat Ulang Tahun"},
            {"title": "Akad", "artist": "Payung Teduh", "album": "Ruang Tunggu"},
        ]

        # Pencocokan sederhana tanpa membedakan huruf besar/kecil.
        if query:
            normalized_query = query.casefold()
            results = [
                song for song in demo_songs
                if normalized_query in song["title"].casefold()
                or normalized_query in song["artist"].casefold()
            ]

    return render_template("search_results.html", results=results, query=query)


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

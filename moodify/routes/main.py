"""Route halaman Moodify."""
from flask import Blueprint, render_template, request
from moodify.services.search_service import search_songs, get_song_detail
from moodify.services.lyrics_service import find_lyrics_snippet
from moodify.services.motivation_service import create_message
"""
Jadi Flask itu sebuah framework python yang digunakan untuk membuat sebuah web sederhana, dalam membuat sebuah web di Flask kita perlu untuk
mendefinisikan sebuah varibel yang menjadi app menggunakan main_bp = Blueprint, membuat kelompok route bernama main, __name__ berguna untuk
memberi tahu flask lokasi dari bluprint in. Ada beberapa fungsi yang cukup banyak digunakan dalam flask contohnya render_template untuk
merender html yang diberikan, ada juga request yang digunakan untuk membuat http request dan juga response (form.get untuk mengambil req dari kita
, ) 
"""
# mengambil fungsi dari file lain

main_bp = Blueprint("main", __name__) # membuat sebuah kelompok route bernama main.bp


@main_bp.get("/") # endpoint root > menampilkan fitur yang ada secara visual
def home():
    return render_template("home.html")


@main_bp.route("/search", methods=["GET", "POST"]) # endpoint search > untuk membuat sebuah request dari pengguna dan mersponse
def search():
    query = ""
    results = []
    error = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        search_type = request.form.get("search_type", "title_artist")
        selected_mood = request.form.get("mood", "")
        results, error, prompt_info = search_songs(query, search_type, selected_mood) # menggunakan fungsi dari file search_servces.py
    else:
        prompt_info = None

    return render_template(
        "search_results.html", results=results, query=query, error=error,
        prompt_info=prompt_info,
    )


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


@main_bp.get("/song/<int:song_id>") # endpoint search > untuk menyimpan pencarian kita menggunakan id yang unik
def song_detail(song_id):
    song, error = get_song_detail(song_id)
    lyrics = None
    message = None
    if song:
        lyrics = find_lyrics_snippet(
            song["title"], song["artist"], song["album"], song["duration"]
        )
        message = create_message("")
    return render_template(
        "song_detail.html", song=song, song_id=song_id, lyrics=lyrics,
        message=message, error=error,
    )

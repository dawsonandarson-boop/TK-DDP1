"""Pencarian lagu lewat iTunes Search API dan normalisasi hasil Moodify."""
import json
import os
import requests

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"


def _prompt_to_keywords(prompt):
    """Fallback lokal sederhana jika Gemini belum dikonfigurasi."""
    ignored = {"lagu", "yang", "buat", "untuk", "aku", "saya", "ingin", "dong", "dengan", "suasana", "hati", "tentang"}
    words = [word.strip(".,!?;:") for word in prompt.split()]
    keywords = [word for word in words if word and word.casefold() not in ignored]
    return " ".join(keywords) or prompt


def understand_prompt(prompt):
    """Pakai Gemini bila dikonfigurasi; selain itu gunakan fallback lokal."""
    fallback = {
        "keywords": _prompt_to_keywords(prompt),
        "mood": _guess_mood(prompt),
        "energy": "sedang",
        "used_gemini": False,
    }
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return fallback

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=(
                "Ubah prompt pengguna menjadi kata pencarian singkat untuk katalog musik. "
                "Jangan menyebut judul atau artis yang tidak diminta. Pilih mood dari "
                "senang, sedih, tenang, semangat, atau netral; energy dari rendah, sedang, "
                "atau tinggi. Prompt: " + prompt
            ),
            config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "keywords": {"type": "STRING"},
                        "mood": {"type": "STRING", "enum": ["senang", "sedih", "tenang", "semangat", "netral"]},
                        "energy": {"type": "STRING", "enum": ["rendah", "sedang", "tinggi"]},
                    },
                    "required": ["keywords", "mood", "energy"],
                },
                "temperature": 0.2,
            },
        )
        parsed = json.loads(response.text)
        keywords = parsed.get("keywords", "").strip()
        if not keywords:
            return fallback
        return {
            "keywords": keywords[:100],
            "mood": parsed.get("mood", "netral"),
            "energy": parsed.get("energy", "sedang"),
            "used_gemini": True,
        }
    except Exception:
        # Pencarian tetap bisa dipakai bila SDK/API/model sedang gagal.
        return fallback


def _guess_mood(text):
    text = text.casefold()
    words_by_mood = {
        "senang": ["senang", "bahagia", "happy", "ceria"],
        "sedih": ["sedih", "galau", "patah hati", "kecewa"],
        "tenang": ["tenang", "santai", "relaks", "tidur", "belajar"],
        "semangat": ["semangat", "energi", "olahraga", "fokus", "kerja"],
    }
    for mood, words in words_by_mood.items():
        if any(word in text for word in words):
            return mood
    return "netral"


def search_songs(query, search_type="title_artist", selected_mood=""):
    """Cari lagu dan kembalikan (daftar_lagu, pesan_error)."""
    query = query.strip()
    if not query:
        return [], None

    prompt_info = understand_prompt(query) if search_type == "prompt" else None
    search_term = prompt_info["keywords"] if prompt_info else query
    if selected_mood:
        search_term = f"{selected_mood} {search_term}".strip()
    params = {
        "term": search_term,
        "media": "music",
        "entity": "song",
        "country": "id",
        "limit": 15,
    }

    try:
        response = requests.get(ITUNES_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return [], "Layanan pencarian iTunes sedang tidak dapat dihubungi. Coba lagi nanti."
    except ValueError:
        return [], "Respons dari layanan pencarian tidak dapat dibaca. Coba lagi nanti."

    songs = []
    for item in payload.get("results", []):
        # Field opsional dapat tidak tersedia untuk sebagian lagu.
        songs.append({
            "id": item.get("trackId"),
            "title": item.get("trackName", "Judul tidak tersedia"),
            "artist": item.get("artistName", "Artis tidak tersedia"),
            "album": item.get("collectionName", "Album tidak tersedia"),
            "cover_url": item.get("artworkUrl100"),
            "preview_url": item.get("previewUrl"),
            "listen_url": item.get("trackViewUrl"),
            "source": "iTunes",
        })

    for song in songs:
        song["prompt_info"] = prompt_info
    return songs, None


def get_song_detail(track_id):
    """Ambil detail lagu dari iTunes berdasarkan trackId."""
    try:
        response = requests.get(
            ITUNES_LOOKUP_URL,
            params={"id": track_id, "country": "id"},
            timeout=10,
        )
        response.raise_for_status()
        items = response.json().get("results", [])
    except (requests.RequestException, ValueError):
        return None, "Detail lagu sedang tidak dapat dimuat. Coba lagi nanti."

    if not items:
        return None, "Lagu tidak ditemukan di iTunes."

    item = items[0]
    return {
        "id": item.get("trackId"),
        "title": item.get("trackName", "Judul tidak tersedia"),
        "artist": item.get("artistName", "Artis tidak tersedia"),
        "album": item.get("collectionName", "Album tidak tersedia"),
        "cover_url": item.get("artworkUrl100"),
        "preview_url": item.get("previewUrl"),
        "listen_url": item.get("trackViewUrl"),
        "duration": item.get("trackTimeMillis", 0) // 1000,
        "genre": item.get("primaryGenreName"),
        "release_date": item.get("releaseDate", "")[:10],
        "source": "iTunes",
    }, None

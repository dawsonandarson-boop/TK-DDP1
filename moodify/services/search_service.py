"""Pencarian lagu lewat iTunes Search API dan normalisasi hasil Moodify."""
import requests

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


def search_songs(query):
    """Cari lagu dan kembalikan (daftar_lagu, pesan_error)."""
    query = query.strip()
    if not query:
        return [], None

    params = {
        "term": query,
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

    return songs, None

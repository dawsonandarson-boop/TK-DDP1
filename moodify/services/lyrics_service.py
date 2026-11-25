"""Adapter LRCLIB untuk mencari kutipan lirik singkat."""
import requests

LRCLIB_GET_URL = "https://lrclib.net/api/get"
CLIENT_HEADERS = {"User-Agent": "Moodify/0.1 (student music discovery project)"}


def find_lyrics_snippet(title, artist, album="", duration=0):
    """Kembalikan maksimal 2 baris/160 karakter, atau None jika tidak tersedia."""
    params = {"track_name": title, "artist_name": artist}
    if album:
        params["album_name"] = album
    if duration:
        params["duration"] = duration

    try:
        response = requests.get(
            LRCLIB_GET_URL, params=params, headers=CLIENT_HEADERS, timeout=10
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        lyrics = response.json().get("plainLyrics") or ""
    except (requests.RequestException, ValueError):
        return None

    lines = [line.strip() for line in lyrics.splitlines() if line.strip()]
    if not lines:
        return None
    snippet = " ".join(lines[:2])
    return snippet[:157].rstrip() + "..." if len(snippet) > 160 else snippet

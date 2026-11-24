"""Konfigurasi aplikasi. Pindahkan secret/API key ke environment variable."""
import os


class Config:
    SECRET_KEY = os.getenv("MOODIFY_SECRET_KEY", "development-only-change-me")
    # TODO: Tambahkan konfigurasi database dan Gemini bila sudah disepakati tim.

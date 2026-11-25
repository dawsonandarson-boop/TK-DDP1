"""Konfigurasi aplikasi. Pindahkan secret/API key ke environment variable."""
import os


class Config:
    SECRET_KEY = os.getenv("MOODIFY_SECRET_KEY", "development-only-change-me")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

"""Kontrak data lagu; sesuaikan bersama tim sebelum mengisi katalog."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Song:
    id: int
    title: str
    artist: str
    mood: Optional[str] = None
    energy: Optional[int] = None
    activity: Optional[str] = None
    preview_url: Optional[str] = None
    listen_url: Optional[str] = None

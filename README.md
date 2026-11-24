# Moodify — kerangka proyek Flask

Folder ini berisi **peta file dan titik sambung**, bukan aplikasi fitur lengkap. Isi `TODO` dibagi untuk dikerjakan tim. Route halaman dasar sudah disiapkan agar setiap bagian punya tempat implementasi.

## Struktur

```text
app.py                         Entry point Flask
moodify/
  __init__.py                  Factory aplikasi dan registrasi blueprint
  config.py                    Konfigurasi/secret
  routes/main.py               URL dan alur request halaman
  services/                    Logika pencarian, rekomendasi, lirik, pesan
  repositories/                Akses katalog lokal dan data sesi
  models/song.py               Bentuk data lagu bersama
templates/                     Satu template per halaman + base
static/css/style.css           Gaya halaman
data/                          Rencana penyimpanan katalog lokal
```

## Pembagian awal untuk 3 orang

1. **Frontend dan alur halaman:** `templates/`, `static/css/style.css`, serta koordinasi field form dengan route di `moodify/routes/main.py`.
2. **Pencarian dan detail lagu:** `moodify/services/search_service.py`, `lyrics_service.py`, `motivation_service.py`, dan halaman hasil/detail. Deezer lalu fallback iTunes; Gemini opsional untuk pemahaman prompt dan pesan motivasi.
3. **Katalog dan rekomendasi:** `models/song.py`, `repositories/`, `recommendation_service.py`, halaman katalog/favorit/riwayat. Skor rekomendasi dihitung dengan aturan Moodify dari katalog lokal.

Sepakati kontrak data lagu dan bentuk hasil service bersama sebelum tiap orang mulai mengisi bagian masing-masing.

## Batas konsep yang harus dipertahankan

- Hasil pencarian eksternal tidak otomatis masuk ke katalog lokal.
- Gemini tidak menghitung skor rekomendasi katalog.
- Favorit dan riwayat terkait sesi browser; aplikasi tidak memakai akun pengguna.
- Detail lagu dapat menggabungkan preview/tautan dengar dari sumber lagu dan kutipan lirik LRCLIB jika tersedia.

## Menjalankan kerangka

Pasang Flask dengan `pip install -r requirements.txt`, lalu jalankan `python app.py`. Route dan template adalah titik awal; service yang belum dibuat memang belum dapat menghasilkan fitur.

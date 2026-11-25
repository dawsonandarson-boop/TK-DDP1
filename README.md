# Moodify — kerangka proyek Flask

Moodify adalah rancangan aplikasi web rekomendasi dan pencarian lagu. Repository ini berisi **kerangka aplikasi**: struktur folder, route dasar, template halaman, serta tempat untuk menambahkan logika fitur. Bagian yang bertanda `TODO` belum selesai dan memang disiapkan untuk dikerjakan oleh tim.

## Daftar isi

- [Struktur folder](#struktur-folder)
- [Penjelasan folder dan file](#penjelasan-folder-dan-file)
- [Cara kerja aplikasi](#cara-kerja-aplikasi)
- [Pembagian tugas untuk 3 orang](#pembagian-tugas-untuk-3-orang)
- [Konsep Moodify yang perlu dijaga](#konsep-moodify-yang-perlu-dijaga)
- [Menjalankan proyek](#menjalankan-proyek)

## Struktur folder

```text
Moodify/
├── app.py
├── requirements.txt
├── README.md
├── moodify/
│   ├── __init__.py
│   ├── config.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── search_service.py
│   │   ├── recommendation_service.py
│   │   ├── lyrics_service.py
│   │   └── motivation_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── catalog_repository.py
│   │   └── session_repository.py
│   └── models/
│       ├── __init__.py
│       └── song.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── search_results.html
│   ├── recommendations.html
│   ├── catalog.html
│   ├── favorites.html
│   ├── history.html
│   └── song_detail.html
├── static/
│   └── css/
│       └── style.css
└── data/
    └── README.md
```

## Penjelasan folder dan file

### File di folder utama

- **`app.py`** — Titik masuk untuk menjalankan aplikasi. File ini membuat aplikasi Flask dari `moodify` dan menyalakan server saat perintah `python app.py` dijalankan.
- **`requirements.txt`** — Daftar library Python yang dibutuhkan. Saat ini Flask sudah dicantumkan. Jika nanti tim memilih library database atau integrasi lain, tambahkan dependensinya di sini.
- **`README.md`** — Panduan proyek ini: struktur kode, cara menjalankan, konsep, dan pembagian pekerjaan.

### `moodify/`: kode aplikasi

Folder ini memisahkan bagian-bagian aplikasi berdasarkan tanggung jawabnya.

- **`moodify/__init__.py`** — Membuat aplikasi Flask melalui fungsi `create_app()` dan mendaftarkan blueprint route. File ini juga memberi tahu Flask bahwa `templates/` dan `static/` berada di folder utama proyek.
- **`moodify/config.py`** — Tempat konfigurasi aplikasi, misalnya secret key, pengaturan database, atau status penggunaan Gemini. Secret/API key sebaiknya dibaca dari environment variable dan tidak ditulis langsung di repository.

#### `moodify/routes/`: alamat halaman dan alur request

Route menghubungkan URL dengan fungsi Python yang menyiapkan halaman. Route juga menjadi penghubung antara form, service, dan template.

- **`routes/__init__.py`** — Penanda bahwa folder `routes` adalah package Python.
- **`routes/main.py`** — Daftar URL utama: beranda, pencarian, rekomendasi, katalog, favorit, riwayat, dan detail lagu. Saat fiturnya dibuat, route akan membaca input, memanggil service yang sesuai, lalu mengirim hasilnya ke template.

#### `moodify/services/`: logika fitur

Service mengerjakan proses fitur. Tujuannya agar logika tidak menumpuk di route atau di dalam HTML.

- **`services/__init__.py`** — Penanda bahwa folder `services` adalah package Python.
- **`services/search_service.py`** — Tempat logika pencarian lagu berdasarkan judul, artis, prompt, atau mood. Rencana alurnya: cari di Deezer, lalu gunakan iTunes jika Deezer tidak memberi hasil. Prompt bebas dapat dibantu Gemini; jika Gemini tidak aktif, gunakan pencocokan kata sederhana.
- **`services/recommendation_service.py`** — Tempat analisis cerita pengguna untuk memperkirakan mood, energi, dan aktivitas, lalu mencocokkannya dengan lagu katalog dan menghitung skor.
- **`services/lyrics_service.py`** — Tempat integrasi LRCLIB untuk mencari kutipan lirik singkat jika tersedia.
- **`services/motivation_service.py`** — Tempat membuat pesan motivasi. Gemini bersifat opsional; aplikasi perlu punya pesan bawaan sebagai fallback.

#### `moodify/repositories/`: akses dan penyimpanan data

Repository bertanggung jawab mengambil atau menyimpan data. Service dapat meminta data lewat repository tanpa perlu tahu detail apakah datanya berasal dari SQLite, file, atau penyimpanan sesi.

- **`repositories/__init__.py`** — Penanda bahwa folder `repositories` adalah package Python.
- **`repositories/catalog_repository.py`** — Tempat membaca daftar lagu dari katalog lokal, menerapkan filter, dan mengambil satu lagu berdasarkan ID.
- **`repositories/session_repository.py`** — Tempat membaca atau memperbarui favorit dan riwayat mood yang terkait dengan sesi browser. Rancangan Moodify tidak memakai akun pengguna.

#### `moodify/models/`: bentuk data

- **`models/__init__.py`** — Penanda bahwa folder `models` adalah package Python.
- **`models/song.py`** — Mendefinisikan bentuk data lagu melalui class `Song`, seperti ID, judul, artis, mood, energi, aktivitas, URL preview, dan URL untuk mendengarkan lagu. Samakan field ini dengan semua anggota tim sebelum mengisi data.

### `templates/`: kerangka HTML halaman

Template adalah file HTML yang dirender Flask untuk ditampilkan di browser. Template sekarang masih bertanda `TODO`; isinya perlu dibuat oleh tim.

- **`base.html`** — Kerangka umum yang dapat dipakai bersama, misalnya navigasi, area konten, dan footer.
- **`home.html`** — Beranda. Rencananya berisi form cari judul/artis, pencarian dengan prompt, pilihan mood, dan form cerita untuk rekomendasi.
- **`search_results.html`** — Tempat menampilkan hasil pencarian Deezer/iTunes.
- **`recommendations.html`** — Tempat menampilkan lagu katalog yang direkomendasikan, skor, dan alasan kecocokannya.
- **`catalog.html`** — Tempat menampilkan dan menyaring lagu dari katalog lokal Moodify.
- **`favorites.html`** — Tempat menampilkan lagu favorit pengguna.
- **`history.html`** — Tempat menampilkan riwayat rekomendasi mood pengguna.
- **`song_detail.html`** — Tempat menampilkan informasi lagu, preview audio jika ada, tautan untuk mendengarkan lagu penuh, kutipan lirik, dan pesan motivasi.

### `static/`: aset tampilan

- **`static/css/style.css`** — Tempat mengatur warna, font, ukuran, jarak, tata letak, dan tampilan responsif untuk layar kecil. CSS mengatur tampilan; konten dan struktur halaman berada di template HTML.

### `data/`: rencana penyimpanan katalog

- **`data/README.md`** — Catatan untuk menentukan format penyimpanan katalog lokal, misalnya SQLite, CSV, atau JSON, beserta field data yang diperlukan. Lagu katalog lokal harus dibedakan dari hasil pencarian Deezer/iTunes.

## Cara kerja aplikasi

Secara umum, alur aplikasi yang akan dikembangkan adalah:

```text
Pengguna mengisi form di template
        ↓
Route membaca input dan menentukan alur
        ↓
Service menjalankan logika fitur
        ↓
Repository mengambil atau menyimpan data jika diperlukan
        ↓
Route mengirim hasil ke template
        ↓
Browser menampilkan halaman
```

Contoh alur rekomendasi: pengguna menulis cerita di beranda → route menerima cerita → recommendation service memperkirakan mood/energi/aktivitas → catalog repository menyediakan lagu lokal → Moodify menghitung skor → halaman rekomendasi menampilkan hasil.

Contoh alur pencarian: pengguna memasukkan judul, artis, prompt, atau memilih mood → route meneruskan permintaan ke search service → service mencari melalui Deezer dan dapat mencoba iTunes sebagai fallback → hasil ditampilkan pada halaman pencarian. Hasil ini tidak otomatis menjadi bagian katalog lokal.

## Pembagian tugas untuk 3 orang

Pembagian ini bisa diubah sesuai kemampuan anggota. Sepakati bentuk data lagu dan bentuk hasil antarbagian sebelum mulai menghubungkan kode.

1. **Frontend dan alur halaman** — Mengisi template di `templates/`, CSS di `static/css/style.css`, serta menyepakati field form dengan route di `moodify/routes/main.py`.
2. **Pencarian dan detail lagu** — Mengerjakan `search_service.py`, `lyrics_service.py`, `motivation_service.py`, serta tampilan hasil pencarian dan detail lagu. Pencarian menggunakan Deezer dengan fallback iTunes; Gemini opsional untuk membantu memahami prompt dan membuat pesan motivasi.
3. **Katalog dan rekomendasi** — Menyepakati model lagu, menyiapkan katalog lokal, mengerjakan repository dan `recommendation_service.py`, serta halaman katalog, favorit, dan riwayat.

## Konsep Moodify yang perlu dijaga

- Pencarian langsung dan rekomendasi katalog adalah dua alur berbeda.
- Hasil pencarian iTunes tidak otomatis disimpan ke katalog lokal Moodify.
- Gemini boleh membantu memahami prompt pencarian dan membuat pesan motivasi jika diaktifkan.
- Skor rekomendasi katalog dihitung oleh aturan Moodify sendiri, tanpa AI atau API eksternal.
- Favorit dan riwayat dikaitkan dengan sesi browser; aplikasi tidak memakai akun pengguna.
- Preview dan tautan dengar ditampilkan jika tersedia; lirik LRCLIB dan pesan motivasi juga bersifat opsional.

## Menjalankan proyek

Pastikan Python sudah terpasang, lalu jalankan perintah berikut dari folder proyek di PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Buka `http://127.0.0.1:5000` di browser. Jika PowerShell memblokir aktivasi virtual environment, gunakan interpreter langsung:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Server dihentikan dari terminal dengan `Ctrl+C`. Halaman saat ini baru kerangka; service berisi `TODO` atau `NotImplementedError`, sehingga fitur belum menghasilkan pencarian atau rekomendasi sungguhan.

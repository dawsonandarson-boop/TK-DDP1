"""Pesan motivasi lokal sederhana sebagai fallback tanpa Gemini."""


def create_message(mood, use_gemini=False):
    # TODO (opsional): tambah Gemini untuk membuat variasi pesan motivasi.
    messages = {
        "senang": "Nikmati momen baik ini dan biarkan musik menemanimu.",
        "sedih": "Pelan-pelan saja. Kamu tidak harus menyelesaikan semuanya hari ini.",
        "tenang": "Ambil waktu untuk bernapas dan menikmati jeda ini.",
        "semangat": "Satu langkah kecil tetap membawamu maju. Teruskan!",
    }
    return messages.get((mood or "").casefold(), "Semoga lagu ini menemani harimu dengan baik.")

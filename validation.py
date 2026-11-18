"""Fungsi validasi input laporan."""
import re

KATEGORI_VALID = ("Jalan berlubang", "Jalan retak", "Aspal mengelupas", "Drainase", "Lainnya")

def validasi_laporan(nama, email, kategori, lokasi, deskripsi):
    """Memastikan seluruh kolom wajib terisi dan email memiliki format benar."""
    if not all(str(x).strip() for x in (nama, email, kategori, lokasi, deskripsi)):
        raise ValueError("Semua kolom laporan wajib diisi.")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
        raise ValueError("Format email tidak valid.")
    if kategori not in KATEGORI_VALID:
        raise ValueError("Kategori kerusakan tidak tersedia.")
    if len(deskripsi.strip()) < 5:
        raise ValueError("Deskripsi minimal 5 karakter.")
    return True

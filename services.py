"""Logika aplikasi: pembuatan ID, pencarian, sorting, filter, dan agregasi."""
from models import Laporan
from validation import validasi_laporan

class LayananLaporan:
    """Mengelola data laporan tanpa bergantung pada tampilan UI."""
    def __init__(self, storage):
        self.storage = storage

    def semua_laporan(self):
        """Mengambil data terbaru dari file."""
        return self.storage.muat_semua()

    def buat_laporan(self, nama, email, kategori, lokasi, deskripsi):
        """Validasi dan menyimpan laporan baru."""
        validasi_laporan(nama, email, kategori, lokasi, deskripsi)
        data = self.storage.muat_semua()
        nomor = max((int(x.id_laporan[3:]) for x in data
                     if x.id_laporan.startswith("SM-") and x.id_laporan[3:].isdigit()),
                    default=0) + 1
        laporan = Laporan(f"SM-{nomor:04d}", nama.strip(), email.strip(),
                          kategori, lokasi.strip(), deskripsi.strip())
        self.storage.tambah(laporan)
        return laporan

    def cari_laporan(self, kata_kunci):
        """Linear search pada ID, nama, kategori, dan lokasi."""
        keyword = kata_kunci.strip().lower()
        data = self.storage.muat_semua()
        if not keyword:
            return data
        hasil = []
        for item in data:
            kolom = (item.id_laporan, item.nama_pelapor, item.kategori, item.lokasi)
            if any(keyword in str(nilai).lower() for nilai in kolom):
                hasil.append(item)
        return hasil

    @staticmethod
    def merge_sort(data, key="tanggal", reverse=False):
        """Mengurutkan data memakai algoritma Merge Sort."""
        if len(data) <= 1:
            return list(data)
        tengah = len(data) // 2
        kiri = LayananLaporan.merge_sort(data[:tengah], key, reverse)
        kanan = LayananLaporan.merge_sort(data[tengah:], key, reverse)
        hasil, i, j = [], 0, 0
        while i < len(kiri) and j < len(kanan):
            a = str(getattr(kiri[i], key, "")).lower()
            b = str(getattr(kanan[j], key, "")).lower()
            ambil_kiri = a >= b if reverse else a <= b
            if ambil_kiri:
                hasil.append(kiri[i]); i += 1
            else:
                hasil.append(kanan[j]); j += 1
        return hasil + kiri[i:] + kanan[j:]

    def filter_laporan(self, **kwargs):
        """Menerima filter fleksibel, misalnya status='Menunggu'."""
        data = self.storage.muat_semua()
        for atribut, nilai in kwargs.items():
            if nilai not in (None, ""):
                data = [x for x in data
                        if str(getattr(x, atribut, "")).lower() == str(nilai).lower()]
        return data

    @staticmethod
    def hitung_ringkasan(*laporan):
        """Menghitung total laporan dan jumlah berdasarkan status."""
        return {
            "total": len(laporan),
            "menunggu": sum(x.status == "Menunggu" for x in laporan),
            "diverifikasi": sum(x.status == "Terverifikasi" for x in laporan),
        }

    def verifikasi(self, id_laporan):
        """Mengubah status laporan menjadi Terverifikasi."""
        data = self.storage.muat_semua()
        ditemukan = False
        for item in data:
            if item.id_laporan == id_laporan:
                item.status = "Terverifikasi"
                ditemukan = True
                break
        if not ditemukan:
            raise ValueError("ID laporan tidak ditemukan.")
        self.storage.simpan_semua(data)

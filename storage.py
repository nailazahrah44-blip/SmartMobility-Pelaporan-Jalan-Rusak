"""Pengelolaan penyimpanan permanen laporan dalam format CSV."""
import csv
from pathlib import Path
from models import Laporan

FIELDNAMES = ["id_laporan", "nama_pelapor", "email", "kategori",
              "lokasi", "deskripsi", "status", "tanggal"]

class PenyimpananLaporan:
    """Membaca dan menulis data laporan menggunakan context manager."""
    def __init__(self, file_path="data/laporan.csv"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._siapkan_file()

    def _siapkan_file(self):
        """Membuat file dan header hanya jika file belum tersedia (mode x)."""
        try:
            with open(self.file_path, "x", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()
        except FileExistsError:
            pass

    def muat_semua(self):
        """Memuat seluruh laporan; file kosong atau rusak ditangani pemanggil."""
        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != FIELDNAMES:
                    raise ValueError("Struktur file CSV tidak sesuai.")
                return [Laporan(**row) for row in reader]
        except FileNotFoundError:
            self._siapkan_file()
            return []
        except (csv.Error, TypeError) as error:
            raise ValueError(f"Data CSV tidak dapat dibaca: {error}") from error

    def tambah(self, laporan):
        """Menambahkan satu laporan baru dengan mode append."""
        with open(self.file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writerow(laporan.to_dict())

    def simpan_semua(self, daftar_laporan):
        """Menulis ulang seluruh data setelah perubahan status (mode write)."""
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(item.to_dict() for item in daftar_laporan)

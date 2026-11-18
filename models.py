"""Model data untuk objek laporan kerusakan jalan."""
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Laporan:
    """Mewakili satu laporan kerusakan jalan."""
    id_laporan: str
    nama_pelapor: str
    email: str
    kategori: str
    lokasi: str
    deskripsi: str
    status: str = "Menunggu"
    tanggal: str = ""

    def __post_init__(self):
        """Mengisi tanggal otomatis jika belum diberikan."""
        if not self.tanggal:
            self.tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        """Mengubah objek laporan menjadi dictionary untuk CSV."""
        return asdict(self)

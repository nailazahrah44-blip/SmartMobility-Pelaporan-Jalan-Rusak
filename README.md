# SMART MOBILITY - Python

Aplikasi desktop pelaporan kerusakan jalan menggunakan Python dan Tkinter.

## Persyaratan
- Python 3.10 atau lebih baru
- Tkinter (umumnya sudah tersedia pada instalasi Python Windows)

## Menjalankan aplikasi
Buka terminal pada folder proyek, lalu jalankan:

```bash
python main.py
```

## Login demo
- Admin: username `admin`, password `admin123`
- Pengguna: isi nama pengguna dan kata sandi sendiri, lalu pilih peran Pengguna.

## Menjalankan unit test
Dari folder utama proyek:

```bash
python -m unittest discover -s tests -v
```

## Struktur folder
- `main.py`: titik masuk aplikasi.
- `ui.py`: antarmuka login, form, tabel, pencarian, sorting, dan verifikasi.
- `models.py`: class/model data Laporan.
- `services.py`: logika bisnis, linear search, Merge Sort, filter, dan agregasi.
- `storage.py`: baca/tulis CSV dengan `with open()`.
- `validation.py`: validasi input.
- `tests/test_services.py`: enam unit test.
- `data/laporan.csv`: penyimpanan permanen laporan.

## Catatan
Aplikasi ini merupakan prototipe akademik. Kredensial admin demo ditulis langsung di kode dan tidak ditujukan untuk sistem produksi. Data koordinat GPS dan unggah foto belum diaktifkan pada versi ini.

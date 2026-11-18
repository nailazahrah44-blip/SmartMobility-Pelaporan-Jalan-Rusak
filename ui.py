"""Antarmuka desktop SMART MOBILITY menggunakan Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
from storage import PenyimpananLaporan
from services import LayananLaporan
from validation import KATEGORI_VALID

class SmartMobilityApp:
    """Mengatur login, form pelaporan, tabel, pencarian, dan verifikasi."""
    def __init__(self, root):
        self.root = root
        self.root.title("SMART MOBILITY | Pelaporan Jalan Rusak")
        self.root.geometry("1120x720")
        self.root.minsize(950, 620)
        self.root.configure(bg="#eef2f7")
        self.layanan = LayananLaporan(PenyimpananLaporan())
        self.nama_login = ""
        self.peran = ""
        self._style()
        self.tampilkan_login()

    def _style(self):
        """Mengatur gaya komponen ttk agar tampilan lebih konsisten."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=28, font=("Arial", 9))
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"))
        style.configure("TButton", padding=7, font=("Arial", 9, "bold"))

    def bersihkan(self):
        """Menghapus seluruh widget pada jendela utama."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def tampilkan_login(self):
        """Menampilkan halaman login pengguna dan admin."""
        self.bersihkan()
        panel = tk.Frame(self.root, bg="white", padx=40, pady=35,
                         highlightbackground="#d7dee8", highlightthickness=1)
        panel.place(relx=.5, rely=.5, anchor="center")
        tk.Label(panel, text="SMART MOBILITY", bg="white", fg="#17365d",
                 font=("Arial", 22, "bold")).pack(pady=(0, 5))
        tk.Label(panel, text="Sistem Pelaporan Kerusakan Jalan", bg="white",
                 fg="#64748b", font=("Arial", 10)).pack(pady=(0, 25))
        tk.Label(panel, text="Nama pengguna", bg="white").pack(anchor="w")
        self.ent_user = ttk.Entry(panel, width=38)
        self.ent_user.pack(pady=(5, 12))
        tk.Label(panel, text="Kata sandi", bg="white").pack(anchor="w")
        self.ent_pass = ttk.Entry(panel, width=38, show="*")
        self.ent_pass.pack(pady=(5, 12))
        tk.Label(panel, text="Masuk sebagai", bg="white").pack(anchor="w")
        self.role_var = tk.StringVar(value="Pengguna")
        ttk.Combobox(panel, textvariable=self.role_var,
                     values=["Pengguna", "Admin"], state="readonly",
                     width=35).pack(pady=(5, 18))
        ttk.Button(panel, text="MASUK", command=self.proses_login).pack(fill="x")
        tk.Label(panel, text="Demo admin: admin / admin123",
                 bg="white", fg="#64748b", font=("Arial", 8)).pack(pady=(15, 0))

    def proses_login(self):
        """Memeriksa kredensial admin atau login pengguna."""
        nama, sandi = self.ent_user.get().strip(), self.ent_pass.get()
        peran = self.role_var.get()
        if not nama or not sandi:
            messagebox.showwarning("Validasi", "Nama pengguna dan kata sandi wajib diisi.")
            return
        if peran == "Admin" and not (nama == "admin" and sandi == "admin123"):
            messagebox.showerror("Login gagal", "Akun admin tidak sesuai.")
            return
        self.nama_login, self.peran = nama, peran
        self.tampilkan_dashboard()

    def tampilkan_dashboard(self):
        """Menyusun form laporan dan tabel data."""
        self.bersihkan()
        header = tk.Frame(self.root, bg="#17365d", padx=20, pady=15)
        header.pack(fill="x")
        tk.Label(header, text="SMART MOBILITY", bg="#17365d", fg="white",
                 font=("Arial", 18, "bold")).pack(side="left")
        tk.Label(header, text=f"{self.nama_login} | {self.peran}",
                 bg="#17365d", fg="white").pack(side="right")
        ttk.Button(header, text="Keluar", command=self.tampilkan_login).pack(side="right", padx=15)

        body = tk.Frame(self.root, bg="#eef2f7", padx=18, pady=15)
        body.pack(fill="both", expand=True)
        form = tk.LabelFrame(body, text="Form Pelaporan Jalan Rusak",
                             bg="white", padx=12, pady=10)
        form.pack(fill="x")
        self.entries = {}
        labels = [("nama", "Nama pelapor"), ("email", "Email"),
                  ("kategori", "Kategori kerusakan"), ("lokasi", "Lokasi"),
                  ("deskripsi", "Deskripsi")]
        for index, (key, label) in enumerate(labels):
            row, col = divmod(index, 3)
            cell = tk.Frame(form, bg="white")
            cell.grid(row=row, column=col, sticky="ew", padx=7, pady=5)
            tk.Label(cell, text=label, bg="white", fg="#334155").pack(anchor="w")
            if key == "kategori":
                widget = ttk.Combobox(cell, values=KATEGORI_VALID, state="readonly")
                widget.set(KATEGORI_VALID[0])
            elif key == "deskripsi":
                widget = ttk.Entry(cell)
            else:
                widget = ttk.Entry(cell)
            widget.pack(fill="x", pady=(3, 0))
            self.entries[key] = widget
        for col in range(3):
            form.grid_columnconfigure(col, weight=1)
        if self.peran == "Pengguna":
            self.entries["nama"].insert(0, self.nama_login)
        else:
            ttk.Label(form, text="Admin dapat memverifikasi laporan pada tabel.",
                      background="white", foreground="#64748b").grid(
                          row=2, column=0, columnspan=3, sticky="w", padx=7, pady=4)
        actions = tk.Frame(body, bg="#eef2f7")
        actions.pack(fill="x", pady=10)
        ttk.Button(actions, text="Kirim Laporan", command=self.kirim_laporan).pack(side="left")
        ttk.Button(actions, text="Bersihkan Form", command=self.bersihkan_form).pack(side="left", padx=8)
        if self.peran == "Admin":
            ttk.Button(actions, text="Verifikasi Laporan Terpilih",
                       command=self.verifikasi_pilihan).pack(side="left", padx=8)

        searchbar = tk.Frame(body, bg="#eef2f7")
        searchbar.pack(fill="x", pady=(4, 8))
        tk.Label(searchbar, text="Cari ID / nama / kategori / lokasi:",
                 bg="#eef2f7").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(searchbar, textvariable=self.search_var, width=32).pack(side="left", padx=8)
        ttk.Button(searchbar, text="Cari", command=self.tampilkan_data).pack(side="left")
        ttk.Button(searchbar, text="Reset", command=self.reset_pencarian).pack(side="left", padx=5)
        tk.Label(searchbar, text="Urutkan:", bg="#eef2f7").pack(side="left", padx=(20, 5))
        self.sort_var = tk.StringVar(value="tanggal")
        ttk.Combobox(searchbar, textvariable=self.sort_var, state="readonly",
                     values=["tanggal", "nama_pelapor", "kategori", "lokasi", "status"],
                     width=17).pack(side="left")
        ttk.Button(searchbar, text="Terapkan", command=self.tampilkan_data).pack(side="left", padx=5)

        table_frame = tk.Frame(body, bg="white")
        table_frame.pack(fill="both", expand=True)
        columns = ("id", "nama", "kategori", "lokasi", "status", "tanggal")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = {"id": "ID Laporan", "nama": "Nama Pelapor",
                    "kategori": "Kategori", "lokasi": "Lokasi",
                    "status": "Status", "tanggal": "Tanggal"}
        widths = {"id": 100, "nama": 150, "kategori": 150,
                  "lokasi": 240, "status": 120, "tanggal": 140}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.summary = tk.Label(body, text="", bg="#eef2f7",
                                fg="#334155", font=("Arial", 9, "bold"))
        self.summary.pack(anchor="w", pady=(8, 0))
        self.tampilkan_data()

    def bersihkan_form(self):
        """Mengosongkan kolom input laporan."""
        for key, widget in self.entries.items():
            if key == "kategori":
                widget.set(KATEGORI_VALID[0])
            else:
                widget.delete(0, tk.END)

    def kirim_laporan(self):
        """Mengambil input, menjalankan validasi, lalu menyimpan laporan."""
        try:
            values = {key: widget.get() for key, widget in self.entries.items()}
            self.layanan.buat_laporan(**values)
            messagebox.showinfo("Berhasil", "Laporan berhasil disimpan.")
            self.bersihkan_form()
            self.tampilkan_data()
        except ValueError as error:
            messagebox.showerror("Input tidak valid", str(error))
        except (OSError, ValueError) as error:
            messagebox.showerror("Penyimpanan gagal", str(error))

    def tampilkan_data(self):
        """Menampilkan hasil pencarian dan sorting ke tabel."""
        try:
            data = self.layanan.cari_laporan(self.search_var.get())
            key = self.sort_var.get()
            data = self.layanan.merge_sort(data, key=key)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for item in data:
                self.tree.insert("", "end", iid=item.id_laporan,
                                 values=(item.id_laporan, item.nama_pelapor,
                                         item.kategori, item.lokasi,
                                         item.status, item.tanggal))
            ringkasan = self.layanan.hitung_ringkasan(*self.layanan.semua_laporan())
            self.summary.config(text=f"Total: {ringkasan['total']}   |   "
                                     f"Menunggu: {ringkasan['menunggu']}   |   "
                                     f"Terverifikasi: {ringkasan['diverifikasi']}")
        except (OSError, ValueError) as error:
            messagebox.showerror("Kesalahan data", str(error))

    def reset_pencarian(self):
        """Menghapus kata kunci dan memuat ulang tabel."""
        self.search_var.set("")
        self.tampilkan_data()

    def verifikasi_pilihan(self):
        """Memverifikasi baris terpilih; hanya tersedia untuk admin."""
        pilihan = self.tree.selection()
        if not pilihan:
            messagebox.showwarning("Pilih laporan", "Pilih satu laporan pada tabel.")
            return
        try:
            self.layanan.verifikasi(pilihan[0])
            messagebox.showinfo("Berhasil", "Status laporan diperbarui.")
            self.tampilkan_data()
        except (OSError, ValueError) as error:
            messagebox.showerror("Gagal", str(error))

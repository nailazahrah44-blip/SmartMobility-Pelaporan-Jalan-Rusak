"""Titik masuk aplikasi SMART MOBILITY."""
import tkinter as tk
from ui import SmartMobilityApp

def main():
    """Membuat jendela utama dan menjalankan aplikasi."""
    root = tk.Tk()
    SmartMobilityApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# main.py
import tkinter as tk
from views.main_window import MainWindow
from estilos import aplicar_estilos

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")  # o 900x600 si querés más compacto
    aplicar_estilos(root)
    app = MainWindow(root)
    root.mainloop()

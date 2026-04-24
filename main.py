# main.py
import tkinter as tk
from views.main_view import MainView
from ui.ui_theme import init_style

def main():
    root = tk.Tk()
    root.title("Turnero Estética")
    root.geometry("1024x700")
    try:
        # Alta-DPI en Windows (opcional)
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    init_style(root)     # << aplica tema y estilos
    MainView(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# ui/ui_theme.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# 🎨 Paleta de colores extraída del logo
COLORS = {
    "bg": "#F8F8F8",        # Fondo principal
    "primary": "#F2A1AC",   # Rosa medio
    "primary_light": "#FCCFD4",  # Rosa claro
    "text": "#000000",      # Negro
    "text_muted": "#6E5759", # Marrón grisáceo
    "surface": "#FFFFFF",  # o "#FFF5F6" para un rosado muy claro

}

FONTS = {
    "title": ("Segoe UI", 18, "bold"),
    "subtitle": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 11)
}

def init_style(root: tk.Tk):
    root.configure(bg=COLORS["bg"])
    style = ttk.Style(root)
    style.theme_use("clam")

    # Frames
    style.configure("App.TFrame", background=COLORS["bg"])

    # Labels
    style.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=FONTS["title"])
    style.configure("Subtitle.TLabel", background=COLORS["bg"], foreground=COLORS["text_muted"], font=FONTS["subtitle"])
    style.configure("Body.TLabel", background=COLORS["bg"], foreground=COLORS["text_muted"], font=FONTS["body"])

    # Botones redondeados
    style.configure("Rounded.TButton",
        font=FONTS["body"],
        padding=(14, 8),
        background=COLORS["primary"],
        foreground=COLORS["text"],
        borderwidth=0,
        relief="flat")
    style.map("Rounded.TButton",
        background=[("active", COLORS["primary_light"])],
        relief=[("pressed", "sunken")])

    # Combobox
    style.configure("TCombobox",
        fieldbackground=COLORS["primary_light"],
        background=COLORS["primary_light"],
        foreground=COLORS["text"])
    root.option_add("*TCombobox*Listbox*Background", COLORS["primary_light"])
    root.option_add("*TCombobox*Listbox*Foreground", COLORS["text"])

def load_logo(frame, size=(50, 50)):
    """Carga y coloca el logo en un frame."""
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        from PIL import Image
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.Resampling.LANCZOS
        raw = Image.open(logo_path).convert("RGBA")
        raw = raw.resize(size, resample)
        img = ImageTk.PhotoImage(raw)
        frame._logo_img = img
        label = tk.Label(frame, image=frame._logo_img, bg=COLORS["bg"])
        label.pack(side="left", padx=10, pady=10)


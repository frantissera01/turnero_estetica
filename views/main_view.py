# views/main_view.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow
import os

from controllers.main_controller import MainController
from ui.ui_theme import init_style, COLORS

class MainView(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg=COLORS["bg"])
        self.controller = MainController(root)
        self.pack(fill="both", expand=True)
        self._logo_img = None  # mantener referencia
        self._build()

    def _build(self):
        # Header
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=16, pady=(16, 8))

        # Logo (esquina sup. izq.)
        logo_path = os.path.join("assets", "logo.png")  # ajustá nombre
        if os.path.exists(logo_path):
            raw = Image.open(logo_path).convert("RGBA")
            raw = raw.resize((44, 44), Image.Resampling.LANCZOS) 
            self._logo_img = ImageTk.PhotoImage(raw)
            tk.Label(header, image=self._logo_img, bg=COLORS["bg"]).pack(side="left")

        ttk.Label(header, text="Las Magnolias ", style="Title.TLabel").pack(side="left", padx=12)

        # Contenedor central (cards)
        wrap = tk.Frame(self, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=16, pady=16)

        nav = ttk.LabelFrame(wrap, text="Navegación", style="H2.TLabel")
        nav.config(labelanchor="n")  # título centrado
        nav.configure(style="Card.TFrame")
        nav.pack(fill="x", pady=8)

        grid = tk.Frame(nav, bg=COLORS["surface"])
        grid.pack(padx=12, pady=12, fill="x")

        # Matriz de botones (2x3 por ejemplo)
        buttons = [
            ("Gestión de Empleados", self.controller.abrir_gestion_empleados),
            ("Gestión de Clientes",   self.controller.abrir_gestion_clientes),
            ("Turnos (Semanal)",      self.controller.abrir_turnos),
            ("Ingreso/Egreso",        self.controller.abrir_horarios),
            ("Planes y Asignaciones", self.controller.abrir_planes),
        ]

        # Grid responsivo
        cols = 3
        for i in range(cols):
            grid.grid_columnconfigure(i, weight=1)

        for idx, (text, cmd) in enumerate(buttons):
            r, c = divmod(idx, cols)
            btn = ttk.Button(grid, text=text, style="Primary.TButton", command=cmd)
            btn.grid(row=r, column=c, padx=8, pady=8, sticky="ew")

        # Pie (opcional)
        footer = tk.Frame(self, bg=COLORS["bg"])
        footer.pack(fill="x", padx=16, pady=(0, 16))
        ttk.Separator(footer, orient="horizontal").pack(fill="x", pady=8)
        tk.Label(footer, text="© 2025 Tu Centro", bg=COLORS["bg"], fg=COLORS["text_muted"]).pack()

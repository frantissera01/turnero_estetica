# views/main_view.py (solo las partes nuevas/ajustadas)
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from controllers.main_controller import MainController
from ui.ui_theme import COLORS

class MainView(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg=COLORS["bg"])
        # controller recibe referencia a esta vista para poder “volver”
        self.controller = MainController(root, self)
        self._logo_img = None
        self.pack(fill="both", expand=True)
        self._build_shell()
        self.render_home()  # muestra el menú principal al inicio

    def _build_shell(self):
        # Header con logo y título (igual que ya tenías)
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=16, pady=(16, 8))

        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            try:
                resample = Image.Resampling.LANCZOS
            except AttributeError:
                resample = Image.Resampling.LANCZOS
            raw = Image.open(logo_path).convert("RGBA").resize((44, 44), resample)
            self._logo_img = ImageTk.PhotoImage(raw)
            tk.Label(header, image=self._logo_img, bg=COLORS["bg"]).pack(side="left")

        ttk.Label(header, text="Turnero Estética", style="Title.TLabel").pack(side="left", padx=12)

        # Contenedor central donde iremos metiendo el home o las sub-vistas
        self.content = tk.Frame(self, bg=COLORS.get("bg", "#FFFFFF"))
        self.content.pack(fill="both", expand=True, padx=16, pady=16)

        # Footer (opcional)
        footer = tk.Frame(self, bg=COLORS["bg"])
        footer.pack(fill="x", padx=16, pady=(0, 16))
        ttk.Separator(footer, orient="horizontal").pack(fill="x", pady=8)
        tk.Label(footer, text="© 2025 Tu Centro", bg=COLORS["bg"], fg=COLORS.get("text_muted", "#6E5759")).pack()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def open_in_content(self, factory):
        """factory(parent) debe devolver el frame/vista a mostrar"""
        self.clear_content()
        factory(self.content)

    # ======= HOME (menú principal) =======
    def render_home(self):
        self.clear_content()

        card = ttk.Frame(self.content, style="Card.TFrame")
        card.pack(fill="x", pady=8)

        ttk.Label(card, text="Navegación", style="Subtitle.TLabel").pack(anchor="w", padx=12, pady=(10, 0))
        grid = tk.Frame(card, bg=COLORS.get("surface", "#FFFFFF"))
        grid.pack(padx=12, pady=12, fill="x")

        buttons = [
            ("Gestión de Empleados", self.controller.abrir_gestion_empleados),
            ("Gestión de Clientes",   self.controller.abrir_gestion_clientes),
            ("Turnos (Semanal)",      self.controller.abrir_turnos),
            ("Ingreso/Egreso",        self.controller.abrir_horarios),
            ("Planes y Asignaciones", self.controller.abrir_planes),
        ]

        cols = 3
        for i in range(cols):
            grid.grid_columnconfigure(i, weight=1)

        for idx, (text, cmd) in enumerate(buttons):
            r, c = divmod(idx, cols)
            btn = ttk.Button(grid, text=text, style="Rounded.TButton", command=cmd)
            btn.grid(row=r, column=c, padx=8, pady=8, sticky="ew")

import tkinter as tk
from PIL import Image, ImageTk

class BotonRedondeado(tk.Canvas):
    def __init__(self, master, texto, comando=None, ancho=180, alto=45, color="#58D68D", color_hover="#45B39D", radio=20, icono_path=None):
        super().__init__(master, width=ancho, height=alto, highlightthickness=0, bg=master["bg"])
        self.comando = comando
        self.color = color
        self.color_hover = color_hover
        self.radio = radio
        self.texto = texto
        self.icono = None
        self.alto = alto
        self.ancho = ancho

        if icono_path:
            imagen = Image.open(icono_path).resize((24, 24), Image.Resampling.LANCZOS)
            self.icono = ImageTk.PhotoImage(imagen)

        self.rect = self.create_round_rect(0, 0, ancho, alto, r=radio, fill=color, outline="")
        self.text_id = self.create_text(ancho//2 + (15 if self.icono else 0), alto//2, text=texto, font=("Segoe UI", 10, "bold"), fill="white")

        if self.icono:
            self.create_image(20, alto//2, image=self.icono)

        # Eventos
        self.bind("<Button-1>", self._click)
        self.bind("<Enter>", self._hover_enter)
        self.bind("<Leave>", self._hover_leave)

    def _click(self, event):
        if self.comando:
            self.comando()

    def _hover_enter(self, event):
        self.itemconfig(self.rect, fill=self.color_hover)
        self.move(self.text_id, 0, 1)  # se hunde levemente
        self.configure(cursor="hand2")  # cambia el cursor

    def _hover_leave(self, event):
        self.itemconfig(self.rect, fill=self.color)
        self.move(self.text_id, 0, -1)  # vuelve a su lugar
        self.configure(cursor="")

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

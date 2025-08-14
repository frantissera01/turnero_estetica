import tkinter as tk
from tkinter import ttk
from controllers.main_controller import MainController

class MainView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.controller = MainController(root)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#f0f0f0")
        titulo = tk.Label(self, text="Turnero Estética", font=("Arial", 20, "bold"), bg="#f0f0f0")
        titulo.pack(pady=20)
        botones = [
            ("Gestión de Empleados", self.controller.abrir_gestion_empleados),
            ("Gestión de Clientes", self.controller.abrir_gestion_clientes),
            ("Ingreso/Egreso Empleados", self.controller.abrir_horarios),
            ("Planes y Asignaciones", self.controller.abrir_planes),
        ]
        
        for texto, comando in botones:
            btn = ttk.Button(self, text=texto, command=comando)
            btn.pack(pady=10, ipadx=10, ipady=5)
import tkinter as tk
from tkinter import ttk

def aplicar_estilos(root):
    estilo = ttk.Style(root)

    # Estilo general
    estilo.theme_use("clam")

    # Colores base
    estilo.configure(".", font=("Segoe UI", 10), foreground="#1C2833", background="#F9F9F9")

    # Botones
    estilo.configure("TButton", padding=6, relief="flat", background="#58D68D", foreground="black")
    estilo.map("TButton",
        background=[("active", "#45B39D")],
        foreground=[("disabled", "#AAB7B8")]
    )

    # Labels
    estilo.configure("TLabel", background="#F9F9F9", font=("Segoe UI", 10))

    # Frame (contenedores)
    estilo.configure("TFrame", background="#F9F9F9")

    # Entry
    estilo.configure("TEntry", padding=5)

    # Treeview (tablas)
    estilo.configure("Treeview",
        background="white",
        foreground="black",
        rowheight=25,
        fieldbackground="white"
    )
    estilo.map("Treeview",
        background=[("selected", "#AED6F1")],
        foreground=[("selected", "black")]
    )

    estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#5DADE2", foreground="white")

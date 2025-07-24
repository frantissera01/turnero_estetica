import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
from datetime import datetime

from views.planes_view import abrir_planes 
from views.turnos.main_view import abrir_turnero
from views.clientes.main_view import abrir_clientes
from views.empleados_view import abrir_empleados

from controllers.horarios_controller import registrar_ingreso, registrar_egreso, listar_empleados_disponibles
from models.horarios_model import empleados_en_turno, obtener_registro_sin_egreso
from models.empleados_model import obtener_empleado_por_id

import os
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Turnos - Centro de Estética")
        self.root.geometry("1000x700")

        # 🖼️ Fondo como imagen de fondo con redimensionamiento fijo
        ruta_fondo = os.path.join("imagenes", "fondo.png")
        imagen = Image.open(ruta_fondo).resize((1000, 700), Image.Resampling.LANCZOS)
        self.fondo_tk = ImageTk.PhotoImage(imagen)

        self.canvas = tk.Canvas(root, width=1000, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.fondo_tk)

        # 🎯 Contenedor principal encima del fondo
        self.contenedor = tk.Frame(self.canvas, bg="#ffffff", highlightthickness=0)
        self.canvas.create_window(500, 350, window=self.contenedor, anchor="center")

        # 📌 Título
        ttk.Label(self.contenedor, text="Menú principal", font=("Arial", 16)).pack(pady=10)

        # 🧭 Frame de botones
        frame_botones = tk.Frame(self.contenedor, bg="#ffffff")
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Gestión de Turnos", command=self.abrir_turnero).grid(row=0, column=0, padx=10)
        ttk.Button(frame_botones, text="Control de Empleados", command=self.abrir_empleados).grid(row=0, column=1, padx=10)
        ttk.Button(frame_botones, text="Gestión de Clientes", command=self.mostrar_clientes).grid(row=0, column=2, padx=10)
        ttk.Button(frame_botones, text="Planes", command=self.abrir_planes).grid(row=0, column=3, padx=10)

        # ⏱️ Ingreso / Egreso
        ttk.Button(frame_botones, text="Marcar Ingreso", command=self.marcar_ingreso).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(frame_botones, text="Marcar Egreso", command=self.marcar_egreso).grid(row=1, column=1, padx=10, pady=5)

       # 🪟 Frame con Scroll para vistas dinámicas
        self.scroll_canvas = tk.Canvas(self.contenedor, bg="#ffffff", highlightthickness=0)
        self.scroll_canvas.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.contenedor, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        # Contenedor real del contenido
        self.frame_contenido = tk.Frame(self.scroll_canvas, bg="#ffffff")
        self.scroll_canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw")

        # Permitir que el canvas actualice el scroll cuando se modifique el contenido
        def actualizar_scroll(event):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

        self.frame_contenido.bind("<Configure>", actualizar_scroll)

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def mostrar_clientes(self):
        self.limpiar_contenido()
        abrir_clientes(self.frame_contenido)

    def abrir_turnero(self):
        self.limpiar_contenido()
        abrir_turnero(self.frame_contenido)

    def abrir_empleados(self):
        self.limpiar_contenido()
        abrir_empleados(self.frame_contenido)

    def abrir_planes(self):
        abrir_planes(self.frame_contenido)

    def marcar_ingreso(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Marcar Ingreso")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Seleccioná un empleado:").pack(pady=10)

        empleados = listar_empleados_disponibles()
        empleados: Any
        seleccion = tk.StringVar()
        opciones = [f"{e['id']} - {e['nombre']}" for e in empleados]
        combo = ttk.Combobox(ventana, values=opciones, textvariable=seleccion)
        combo.pack()

        def confirmar():
            seleccionado = seleccion.get()
            if seleccionado:
                emp_id = int(seleccionado.split(" - ")[0])
                registrar_ingreso(emp_id)
                messagebox.showinfo("Éxito", "Ingreso registrado.")
                ventana.destroy()

        tk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)

    def mostrar_modal_confirmacion_egreso(self, empleado_id, nombre_empleado, tarifa_por_hora):
        registro = obtener_registro_sin_egreso(empleado_id)
        if not registro:
            messagebox.showerror("Error", "No hay ingreso registrado para este empleado.")
            return

        fecha = registro["fecha"]
        hora_ingreso = registro["hora_ingreso"]
        hora_actual = datetime.now().strftime("%H:%M:%S")

        formato = "%H:%M:%S"
        t1 = datetime.strptime(str(hora_ingreso), formato)
        t2 = datetime.strptime(hora_actual, formato)
        horas_trabajadas = round((t2 - t1).total_seconds() / 3600, 2)
        total_dia = round(horas_trabajadas * tarifa_por_hora, 2)

        modal = tk.Toplevel(self.root)
        modal.title("Confirmar egreso")
        modal.geometry("300x250")
        modal.grab_set()

        info = (
            f"Empleado: {nombre_empleado}\n"
            f"Fecha: {fecha}\n"
            f"Hora ingreso: {hora_ingreso}\n"
            f"Hora egreso: {hora_actual}\n"
            f"Horas trabajadas: {horas_trabajadas:.2f}\n"
            f"Monto del día: ${total_dia:.2f}"
        )

        tk.Label(modal, text=info, justify="left").pack(padx=10, pady=10)

        def confirmar():
            registrar_egreso(empleado_id)
            messagebox.showinfo("Egreso registrado", "El egreso fue registrado exitosamente.")
            modal.destroy()

        def cancelar():
            modal.destroy()

        tk.Button(modal, text="Confirmar", bg="green", fg="white", command=confirmar).pack(side="left", padx=20, pady=10)
        tk.Button(modal, text="Cancelar", bg="red", fg="white", command=cancelar).pack(side="right", padx=20, pady=10)

    def marcar_egreso(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Marcar Egreso")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Empleados en turno:").pack(pady=10)

        empleados = empleados_en_turno()
        if not empleados:
            messagebox.showinfo("Aviso", "No hay empleados con ingreso marcado.")
            ventana.destroy()
            return

        seleccion = tk.StringVar()
        empleados: Any
        opciones = [f"{e['id']} - {e['nombre']}" for e in empleados]
        combo = ttk.Combobox(ventana, values=opciones, textvariable=seleccion)
        combo.pack()

        def confirmar():
            seleccionado = seleccion.get()
            if seleccionado:
                emp_id = int(seleccionado.split(" - ")[0])
                nombre_empleado = seleccionado.split(" - ")[1]
                empleado = obtener_empleado_por_id(emp_id)
                empleado: Any
                tarifa = float(empleado["tarifa_por_hora"])
                ventana.destroy()
                self.mostrar_modal_confirmacion_egreso(emp_id, nombre_empleado, tarifa)

        tk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)

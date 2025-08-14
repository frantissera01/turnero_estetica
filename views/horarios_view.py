import tkinter as tk
from tkinter import ttk, messagebox
from controllers.horarios_controller import HorariosController

class HorariosView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.controller = HorariosController(self)
        self.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        tk.Label(self, text="Registro de Ingreso/Egreso", font=("Arial", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Empleado:").grid(row=0, column=0, padx=5)
        self.cmb_empleado = ttk.Combobox(frame, width=30, state="readonly")
        self.cmb_empleado.grid(row=0, column=1, padx=5)

        empleados = self.controller.lista_empleados()
        def formatear_empleado(e):
            if isinstance(e, dict):
                return f"{e.get('id')} - {e.get('nombre', '')} {e.get('apellido', '')}"
            elif isinstance(e, (list, tuple)) and len(e) >= 3:
                return f"{e[0]} - {e[1]} {e[2]}"
            return ""

        opciones = [formatear_empleado(e) for e in empleados]
        self.cmb_empleado["values"] = opciones
        btn_ingreso = ttk.Button(frame, text="Registrar Ingreso", command=self._registrar_ingreso)
        btn_ingreso.grid(row=1, column=0, pady=10, padx=5)

        btn_egreso = ttk.Button(frame, text="Registrar Egreso", command=self._registrar_egreso)
        btn_egreso.grid(row=1, column=1, pady=10, padx=5)

    def _registrar_ingreso(self):
        if not self.cmb_empleado.get():
            self.alerta("Seleccione un empleado.")
            return
        empleado_id = int(self.cmb_empleado.get().split(" - ")[0])
        self.controller.registrar_ingreso(empleado_id)

    def _registrar_egreso(self):
        if not self.cmb_empleado.get():
            self.alerta("Seleccione un empleado.")
            return
        empleado_id = int(self.cmb_empleado.get().split(" - ")[0])
        self.controller.registrar_egreso(empleado_id)

    def alerta(self, mensaje):
        messagebox.showinfo("Información", mensaje)

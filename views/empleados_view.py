import tkinter as tk
from tkinter import ttk, messagebox
from controllers.empleados_controller import EmpleadosController
from ui.ui_theme import COLORS

class EmpleadosView(tk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent, bg=COLORS.get("bg", "#FFFFFF"))
        self.on_back = on_back
        self.pack(fill="both", expand=True)
        self._build()
        self.controller = EmpleadosController(self)

    def _build(self):
        header = tk.Frame(self, bg=COLORS.get("bg", "#FFFFFF"))
        header.pack(fill="x", padx=10, pady=(10, 0))
        ttk.Button(header, text="← Volver", style="Rounded.TButton",
                   command=(self.on_back or (lambda: None))).pack(side="left")
        
        cuerpo = tk.Frame(self, bg=COLORS.get("bg", "#FFFFFF"))
        cuerpo.pack(fill="both", expand=True, padx=10, pady=10)
        
        form = tk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)
        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_tarifa = tk.StringVar()

        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_nombre, width=25).grid(row=0, column=1, padx=5)
        ttk.Label(form, text="Apellido").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.var_apellido, width=25).grid(row=0, column=3, padx=5)
        ttk.Label(form, text="Tarifa/hora").grid(row=0, column=4, sticky="w")
        ttk.Entry(form, textvariable=self.var_tarifa, width=10).grid(row=0, column=5, padx=5)

        btns = tk.Frame(self)
        btns.pack(fill="x", padx=10)
        ttk.Button(btns, text="Nuevo", command=self._registrar).pack(side="left", padx=5)
        ttk.Button(btns, text="Editar", command=self._editar).pack(side="left", padx=5)
        ttk.Button(btns, text="Eliminar", command=self._eliminar).pack(side="left", padx=5)
        ttk.Button(btns, text="Pagar", command=self._abrir_pagos).pack(side="left", padx=5) 

        cols = ("id", "nombre", "apellido", "tarifa_hora")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=14)
        headers = ("ID", "Nombre", "Apellido",  "Tarifa/Hora")
        for c, t in zip(cols, headers):
            self.tree.heading(c, text=t)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self._cargar_desde_tabla)

    def _limpiar(self):
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_tarifa.set("0")

    def mostrar_empleados(self, empleados):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for emp in empleados:
            self.tree.insert("", "end", values=(emp["id"], emp["nombre"], emp["apellido"], emp["tarifa_hora"]))

    def _cargar_desde_tabla(self, _evt=None):
        item = self.tree.focus()
        if not item:
            return
        vals = self.tree.item(item, "values")
        self.var_id.set(vals[0])
        self.var_nombre.set(vals[1])
        self.var_apellido.set(vals[2])
        self.var_tarifa.set(vals[3])

    def _registrar(self):
        datos = {
            "id": None,
            "nombre": self.var_nombre.get().strip(),
            "apellido": self.var_apellido.get().strip(),
            "tarifa_hora": float(self.var_tarifa.get() or 0)
        }
        if not datos["nombre"] or not datos["apellido"]:
            messagebox.showerror("Error", "Nombre, Apellido son obligatorios")
            return
        self.controller.guardar(datos)  # INSERT
        self._limpiar()

    def _editar(self):
        if not self.var_id.get():
            messagebox.showinfo("Info", "Seleccioná un empleado de la lista")
            return
        datos = {
            "id": int(self.var_id.get()),
            "nombre": self.var_nombre.get().strip(),
            "apellido": self.var_apellido.get().strip(),
            "tarifa_hora": float(self.var_tarifa.get() or 0)
        }
        self.controller.guardar(datos)  # UPDATE
        self._limpiar()

    def _eliminar(self):
        if not self.var_id.get():
            messagebox.showinfo("Info", "Seleccioná un empleado de la tabla")
            return
        self.controller.eliminar(int(self.var_id.get()))
        self._limpiar()

    def _abrir_pagos(self):
        PagosDialog(self, self.controller)

class PagosDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.title("Pagos a empleados")
        self.controller = controller
        self.resizable(False, False)
        self._build()
        # cargar saldos inicial
        self.controller.view = self  # para usar mostrar_saldos/alerta aquí
        self.controller.cargar_saldos()

    def _build(self):
        frm = ttk.LabelFrame(self, text="Saldos pendientes")
        frm.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("empleado_id", "empleado", "devengado", "pagado", "saldo")
        self.tree = ttk.Treeview(frm, columns=cols, show="headings", height=10)
        headers = ("ID", "Empleado", "Devengado", "Pagado", "Saldo")
        for c, t in zip(cols, headers):
            self.tree.heading(c, text=t)
            w = 90 if c != "empleado" else 220
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        foot = tk.Frame(self)
        foot.pack(fill="x", padx=10, pady=(0,10))

        tk.Label(foot, text="Monto a pagar:").pack(side="left")
        self.ent_monto = ttk.Entry(foot, width=12)
        self.ent_monto.pack(side="left", padx=6)

        ttk.Button(foot, text="Abonar parcial", command=self._pagar_parcial).pack(side="left", padx=4)
        ttk.Button(foot, text="Abonar TOTAL",   command=self._pagar_total).pack(side="left", padx=4)

        ttk.Button(foot, text="Cerrar", command=self.destroy).pack(side="right")

    # Hooks para que el controller nos “inyecte” datos
    def mostrar_saldos(self, data):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for d in data:
            self.tree.insert("", "end", values=(
                d["empleado_id"],
                d["empleado"],
                f"{d['devengado']:.2f}",
                f"{d['pagado']:.2f}",
                f"{d['saldo']:.2f}",
            ))

    def alerta(self, msg):
        messagebox.showinfo("Información", msg)

    def _get_selected_empleado(self):
        it = self.tree.focus()
        if not it:
            self.alerta("Seleccioná un empleado de la lista.")
            return None
        vals = self.tree.item(it, "values")
        try:
            return int(str(vals[0]))
        except Exception:
            self.alerta("ID inválido.")
            return None

    def _pagar_total(self):
        empleado_id = self._get_selected_empleado()
        if empleado_id is None:
            return
        self.controller.pagar_total(empleado_id)

    def _pagar_parcial(self):
        empleado_id = self._get_selected_empleado()
        if empleado_id is None:
            return
        try:
            monto = float(self.ent_monto.get().strip().replace(",", "."))
        except Exception:
            self.alerta("Monto inválido.")
            return
        self.controller.pagar_parcial(empleado_id, monto)

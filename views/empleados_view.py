import tkinter as tk
from tkinter import ttk, messagebox
from controllers.empleados_controller import EmpleadosController

class EmpleadosView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.controller = EmpleadosController(self)
        self.pack(fill="both", expand=True)
        self._build()
        self.controller.cargar_empleados()

    def _build(self):
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
        ttk.Button(btns, text="Nuevo", command=self._limpiar).pack(side="left", padx=5)
        ttk.Button(btns, text="Guardar", command=self._guardar).pack(side="left", padx=5)
        ttk.Button(btns, text="Eliminar", command=self._eliminar).pack(side="left", padx=5)

        cols = ("id", "nombre", "apellido", "tarifa_hora")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.upper())
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self._cargar_desde_tabla)

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

    def _limpiar(self):
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_tarifa.set("")

    def _guardar(self):
        try:
            datos = {
                "id": int(self.var_id.get()) if self.var_id.get() else None,
                "nombre": self.var_nombre.get().strip(),
                "apellido": self.var_apellido.get().strip(),
                "tarifa": float(self.var_tarifa.get())
            }
        except ValueError:
            messagebox.showerror("Error", "Tarifa debe ser numérica")
            return
        self.controller.guardar(datos)
        self._limpiar()

    def _eliminar(self):
        if not self.var_id.get():
            messagebox.showinfo("Info", "Seleccioná un empleado de la tabla")
            return
        self.controller.eliminar(int(self.var_id.get()))
        self._limpiar()
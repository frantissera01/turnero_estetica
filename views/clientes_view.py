import tkinter as tk
from tkinter import ttk, messagebox
from controllers.clientes_controller import ClientesController


class ClientesView(tk.Frame):
    ESTADOS = ("PENDIENTE", "PAGO")

    def __init__(self, root, on_back=None):
        super().__init__(root)
        self.controller = ClientesController(self)
        self.on_back = on_back  # callback para volver al menú
        self.pack(fill="both", expand=True)
        self._build()
        self.controller.cargar()

    def _build(self):
        # Header con botón Volver
        header = tk.Frame(self)
        header.pack(fill="x", padx=10, pady=(10, 0))

        if self.on_back:
            ttk.Button(header, text="← Volver", command=self.on_back).pack(side="left")

        # --- Formulario ---
        form = tk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)

        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_tel = tk.StringVar()
        self.var_doc = tk.StringVar()
        self.var_ses = tk.StringVar(value="0")
        self.var_estado = tk.StringVar(value=self.ESTADOS[0])

        r = 0
        ttk.Label(form, text="Nombre").grid(row=r, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_nombre, width=20).grid(row=r, column=1, padx=5)
        ttk.Label(form, text="Apellido").grid(row=r, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.var_apellido, width=20).grid(row=r, column=3, padx=5)
        r += 1
        ttk.Label(form, text="Teléfono").grid(row=r, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_tel, width=20).grid(row=r, column=1, padx=5)
        ttk.Label(form, text="Documento").grid(row=r, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.var_doc, width=20).grid(row=r, column=3, padx=5)
        r += 1
        ttk.Label(form, text="Sesiones restantes").grid(row=r, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_ses, width=10).grid(row=r, column=1, padx=5)
        ttk.Label(form, text="Estado pago").grid(row=r, column=2, sticky="w")
        cmb = ttk.Combobox(form, textvariable=self.var_estado, values=self.ESTADOS, state="readonly", width=17)
        cmb.grid(row=r, column=3, padx=5)

        # --- Botones ---
        btns = tk.Frame(self)
        btns.pack(fill="x", padx=10)
        ttk.Button(btns, text="Nuevo", command=self._limpiar).pack(side="left", padx=5)
        ttk.Button(btns, text="Guardar", command=self._guardar).pack(side="left", padx=5)
        ttk.Button(btns, text="Eliminar", command=self._eliminar).pack(side="left", padx=5)

        # --- Tabla ---
        cols = ("id", "nombre", "apellido", "telefono", "documento", "sesiones_restantes", "estado_pago")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.upper())
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self._cargar_desde_tabla)

    def mostrar_clientes(self, clientes):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for cl in clientes:
            self.tree.insert(
                "",
                "end",
                values=(
                    cl["id"],
                    cl["nombre"],
                    cl["apellido"],
                    cl.get("telefono"),
                    cl["documento"],
                    cl.get("sesiones_restantes", 0),
                    cl.get("estado_pago", "PENDIENTE"),
                ),
            )

    def _cargar_desde_tabla(self, _evt=None):
        item = self.tree.focus()
        if not item:
            return
        vals = self.tree.item(item, "values")
        self.var_id.set(vals[0])
        self.var_nombre.set(vals[1])
        self.var_apellido.set(vals[2])
        self.var_tel.set(vals[3])
        self.var_doc.set(vals[4])
        self.var_ses.set(vals[5])
        self.var_estado.set(vals[6])

    def _limpiar(self):
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_tel.set("")
        self.var_doc.set("")
        self.var_ses.set("0")
        self.var_estado.set(self.ESTADOS[0])

    def _guardar(self):
        try:
            ses = int(self.var_ses.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Sesiones restantes debe ser un número entero")
            return
        datos = {
            "id": int(self.var_id.get()) if self.var_id.get() else None,
            "nombre": self.var_nombre.get().strip(),
            "apellido": self.var_apellido.get().strip(),
            "telefono": self.var_tel.get().strip(),
            "documento": self.var_doc.get().strip(),
            "sesiones": ses,
            "estado_pago": self.var_estado.get(),
        }
        if not datos["nombre"] or not datos["apellido"] or not datos["documento"]:
            messagebox.showerror("Error", "Nombre, Apellido y Documento son obligatorios")
            return
        self.controller.guardar(datos)
        self._limpiar()

    def _eliminar(self):
        if not self.var_id.get():
            messagebox.showinfo("Info", "Seleccioná un cliente de la tabla")
            return
        self.controller.eliminar(int(self.var_id.get()))
        self._limpiar()

import tkinter as tk
from tkinter import ttk, messagebox
try:
    from ui.ui_theme import COLORS
except Exception:
    COLORS = {"bg": "#FFFFFF"}  # fallback si no está el tema
from controllers.planes_controller import PlanesController


class PlanesView(tk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent, bg=COLORS.get("bg", "#FFFFFF"))
        self.on_back = on_back
        self.controller = PlanesController(self)
        self.pack(fill="both", expand=True)
        self._build_shell()
        self._build_tabs()
        # Carga inicial de datos
        self.controller.cargar_planes()
        self.controller.cargar_asignaciones()
        self._cargar_combos()

    def _build_shell(self):
        # Header con botón Volver
        header = tk.Frame(self, bg=COLORS.get("bg", "#FFFFFF"))
        header.pack(fill="x", padx=10, pady=(10, 0))
        ttk.Button(
            header,
            text="← Volver",
            style="Rounded.TButton",
            command=(self.on_back or (lambda: None))
        ).pack(side="left")

    def _build_tabs(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.frm_planes = tk.Frame(nb, bg=COLORS.get("bg", "#FFFFFF"))
        self.frm_asig   = tk.Frame(nb, bg=COLORS.get("bg", "#FFFFFF"))
        nb.add(self.frm_planes, text="Planes")
        nb.add(self.frm_asig,   text="Asignaciones")

        # --- Tab Planes (conserva tu UI si ya la tenías) ---
        top = tk.Frame(self.frm_planes, bg=COLORS.get("bg", "#FFFFFF"))
        top.pack(fill="x", padx=10, pady=10)

        cols = ("id", "nombre", "descripcion", "total", "precio")
        self.tree_planes = ttk.Treeview(self.frm_planes, columns=cols, show="headings", height=10)
        for c, t in zip(cols, ("ID","Nombre","Descripción","Total sesiones","Precio")):
            self.tree_planes.heading(c, text=t)
            self.tree_planes.column(c, width=120 if c!="descripcion" else 240, anchor="w")
        self.tree_planes.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree_planes.bind("<<TreeviewSelect>>", self._on_sel_plan)

        form = ttk.LabelFrame(self.frm_planes, text="Datos del plan")
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Nombre:", bg=COLORS.get("bg", "#FFFFFF")).grid(row=0, column=0, sticky="e", padx=5, pady=3)
        tk.Label(form, text="Descripción:", bg=COLORS.get("bg", "#FFFFFF")).grid(row=1, column=0, sticky="e", padx=5, pady=3)
        tk.Label(form, text="Total sesiones:", bg=COLORS.get("bg", "#FFFFFF")).grid(row=2, column=0, sticky="e", padx=5, pady=3)
        tk.Label(form, text="Precio:", bg=COLORS.get("bg", "#FFFFFF")).grid(row=3, column=0, sticky="e", padx=5, pady=3)

        self.ent_plan_id = tk.Entry(form, width=8)
        self.ent_nombre  = tk.Entry(form, width=40)
        self.ent_desc    = tk.Entry(form, width=60)
        self.ent_total   = tk.Entry(form, width=10)
        self.ent_precio  = tk.Entry(form, width=12)

        self.ent_plan_id.grid(row=0, column=2, padx=5); self.ent_plan_id.config(state="readonly")
        self.ent_nombre.grid(row=0, column=1, padx=5)
        self.ent_desc.grid(row=1, column=1, columnspan=2, sticky="we", padx=5)
        self.ent_total.grid(row=2, column=1, padx=5)
        self.ent_precio.grid(row=3, column=1, padx=5)

        btns = tk.Frame(form, bg=COLORS.get("bg", "#FFFFFF")); btns.grid(row=4, column=0, columnspan=3, pady=6)
        ttk.Button(btns, text="Nuevo",   style="Rounded.TButton", command=self._nuevo_plan).pack(side="left", padx=4)
        ttk.Button(btns, text="Guardar", style="Rounded.TButton", command=self._guardar_plan).pack(side="left", padx=4)
        ttk.Button(btns, text="Eliminar",style="Rounded.TButton", command=self._eliminar_plan).pack(side="left", padx=4)

        # --- Tab Asignaciones (conserva tu UI si ya la tenías) ---
        top2 = ttk.LabelFrame(self.frm_asig, text="Asignar plan a clienta")
        top2.pack(fill="x", padx=10, pady=10)

        tk.Label(top2, text="Cliente:", bg=COLORS.get("bg", "#FFFFFF")).grid(row=0, column=0, padx=5, pady=3, sticky="e")
        tk.Label(top2, text="Plan:", bg=COLORS.get("bg", "#FFFFFF")).grid(row=0, column=2, padx=5, pady=3, sticky="e")
        tk.Label(top2, text="Fecha inicio (YYYY-MM-DD):", bg=COLORS.get("bg", "#FFFFFF")).grid(row=1, column=0, padx=5, pady=3, sticky="e")

        self.cmb_cliente = ttk.Combobox(top2, state="readonly", width=35)
        self.cmb_plan    = ttk.Combobox(top2, state="readonly", width=35)
        self.ent_fecha   = tk.Entry(top2, width=14)

        self.cmb_cliente.grid(row=0, column=1, padx=5)
        self.cmb_plan.grid(row=0, column=3, padx=5)
        self.ent_fecha.grid(row=1, column=1, padx=5, sticky="w")

        ttk.Button(top2, text="Asignar", style="Rounded.TButton", command=self._asignar).grid(row=1, column=3, padx=5)

        cols2 = ("id","cliente","plan","fecha_inicio","usadas","total","restantes")
        self.tree_asig = ttk.Treeview(self.frm_asig, columns=cols2, show="headings", height=10)
        headers = ("ID","Cliente","Plan","Inicio","Usadas","Total","Restantes")
        for c, t in zip(cols2, headers):
            self.tree_asig.heading(c, text=t)
            self.tree_asig.column(c, width=110 if c not in ("cliente","plan") else 180, anchor="w")
        self.tree_asig.pack(fill="both", expand=True, padx=10, pady=8)

        btns2 = tk.Frame(self.frm_asig, bg=COLORS.get("bg", "#FFFFFF"))
        btns2.pack(pady=6)
        ttk.Button(btns2, text="Marcar sesión usada", style="Rounded.TButton", command=self._marcar).pack(side="left", padx=4)
        ttk.Button(btns2, text="Revertir sesión",     style="Rounded.TButton", command=self._revertir).pack(side="left", padx=4)
        ttk.Button(btns2, text="Eliminar asignación", style="Rounded.TButton", command=self._eliminar_asignacion).pack(side="left", padx=4)

    # ====== Métodos existentes de tu vista (mantén tus implementaciones) ======
    def _on_sel_plan(self, _evt):
        it = self.tree_planes.focus()
        if not it: return
        vals = self.tree_planes.item(it, "values")
        self._set_readonly(self.ent_plan_id, vals[0])
        self.ent_nombre.delete(0, tk.END); self.ent_nombre.insert(0, vals[1])
        self.ent_desc.delete(0, tk.END);   self.ent_desc.insert(0, vals[2])
        self.ent_total.delete(0, tk.END);  self.ent_total.insert(0, vals[3])
        self.ent_precio.delete(0, tk.END); self.ent_precio.insert(0, vals[4])

    def _nuevo_plan(self):
        self._set_readonly(self.ent_plan_id, "")
        for e in (self.ent_nombre, self.ent_desc, self.ent_total, self.ent_precio):
            e.delete(0, tk.END)

    def _guardar_plan(self):
        pid = self.ent_plan_id.get().strip()
        nombre = self.ent_nombre.get().strip()
        desc   = self.ent_desc.get().strip()
        total  = self.ent_total.get().strip() or "0"
        precio = self.ent_precio.get().strip() or "0"
        if pid:
            self.controller.actualizar_plan(int(pid), nombre, desc, int(total), precio)
        else:
            self.controller.crear_plan(nombre, desc, int(total), precio)

    def _eliminar_plan(self):
        pid = self.ent_plan_id.get().strip()
        if not pid:
            self.alerta("Seleccioná un plan.")
            return
        self.controller.eliminar_plan(int(pid))
        self._nuevo_plan()

    def _cargar_combos(self):
        clientes = self.controller.cargar_combo_clientes()
        planes   = self.controller.cargar_combo_planes()

        def fmt_cliente(c):
            if isinstance(c, dict):
                return f"{c.get('id')} - {c.get('apellido','')}, {c.get('nombre','')}"
            elif isinstance(c, (list,tuple)) and len(c)>=3:
                return f"{c[0]} - {c[2]}, {c[1]}"
            return ""
        def fmt_plan(p):
            if isinstance(p, dict):
                return f"{p.get('id')} - {p.get('nombre','')}"
            elif isinstance(p, (list,tuple)) and len(p)>=2:
                return f"{p[0]} - {p[1]}"
            return ""

        self.cmb_cliente["values"] = [fmt_cliente(c) for c in clientes]
        self.cmb_plan["values"]    = [fmt_plan(p) for p in planes]

    def mostrar_planes(self, planes):
        for i in self.tree_planes.get_children():
            self.tree_planes.delete(i)
        for p in planes:
            if isinstance(p, dict):
                vals = (p.get("id"), p.get("nombre",""), p.get("descripcion",""),
                        p.get("total_sesiones",0), p.get("precio",0))
            else:
                vals = (p[0], p[1], p[2], p[3], p[4])
            self.tree_planes.insert("", "end", values=vals)

    def mostrar_asignaciones(self, datos):
        for i in self.tree_asig.get_children():
            self.tree_asig.delete(i)
        for a in datos:
            fi = a.get("fecha_inicio")
            fi_str = fi.isoformat() if hasattr(fi, "isoformat") else (str(fi) if fi is not None else "")
            self.tree_asig.insert("", "end", values=(
                a["id"], a["cliente"], a["plan"], fi_str, a["usadas"], a["total"], a["restantes"]
            ))

    def alerta(self, msg):
        messagebox.showinfo("Información", msg)

    def _set_readonly(self, entry, value):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="readonly")

    def _asignar(self):
        if not self.cmb_cliente.get() or not self.cmb_plan.get() or not self.ent_fecha.get().strip():
            self.alerta("Completá cliente, plan y fecha.")
            return
        cliente_id = int(self.cmb_cliente.get().split(" - ")[0])
        plan_id    = int(self.cmb_plan.get().split(" - ")[0])
        fecha_ini  = self.ent_fecha.get().strip()
        self.controller.asignar_plan(cliente_id, plan_id, fecha_ini)

    def _marcar(self):
        it = self.tree_asig.focus()
        if not it:
            self.alerta("Seleccioná una asignación.")
            return
        asign_id = int(str(self.tree_asig.item(it, "values")[0]))
        self.controller.marcar_uso(asign_id)

    def _revertir(self):
        it = self.tree_asig.focus()
        if not it:
            self.alerta("Seleccioná una asignación.")
            return
        asign_id = int(str(self.tree_asig.item(it, "values")[0]))
        self.controller.revertir_uso(asign_id)

    def _eliminar_asignacion(self):
        it = self.tree_asig.focus()
        if not it:
            self.alerta("Seleccioná una asignación.")
            return
        asign_id = int(str(self.tree_asig.item(it, "values")[0]))
        self.controller.eliminar_asignacion(asign_id)

# views/horarios_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.horarios_controller import HorariosController

try:
    from ui.ui_theme import COLORS
    BG = COLORS.get("bg", "#FFFFFF")
    BTN_STYLE = "Rounded.TButton"
except Exception:
    BG = "#FFFFFF"
    BTN_STYLE = "TButton"


class HorariosView(tk.Frame):
    def __init__(self, parent, on_back=None):
        super().__init__(parent, bg=BG)
        self.on_back = on_back
        self.controller = HorariosController(self)
        self._items_by_emp = {}  # empleado_id -> item_id en Treeview
        self._ingresos_str = {}  # empleado_id -> "HH:MM:SS" (para crono)
        self._timer_job = None
        self.pack(fill="both", expand=True)
        self._build()
        self.controller.cargar_estado_hoy()

    def _build(self):
        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=10, pady=(10, 0))
        if self.on_back:
            ttk.Button(header, text="← Volver", style=BTN_STYLE,
                       command=self.on_back).pack(side="left")

        tk.Label(self, text="Registro de Ingreso/Egreso", font=("Arial", 16, "bold"), bg=BG).pack(pady=10)

        # Selección y botones
        frame = tk.Frame(self, bg=BG)
        frame.pack(pady=10)

        tk.Label(frame, text="Empleado:", bg=BG).grid(row=0, column=0, padx=5, sticky="e")
        self.cmb_empleado = ttk.Combobox(frame, width=30, state="readonly")
        self.cmb_empleado.grid(row=0, column=1, padx=5)

        # Cargar empleados
        empleados = self.controller.lista_empleados()
        def fmt_emp(e):
            if isinstance(e, dict):
                return f"{e.get('id')} - {e.get('nombre','')} {e.get('apellido','')}"
            elif isinstance(e, (list, tuple)) and len(e) >= 3:
                return f"{e[0]} - {e[1]} {e[2]}"
            return ""
        self.cmb_empleado["values"] = [fmt_emp(e) for e in empleados]

        ttk.Button(frame, text="Registrar Ingreso", style=BTN_STYLE, command=self._registrar_ingreso)\
            .grid(row=1, column=0, pady=10, padx=5)
        ttk.Button(frame, text="Registrar Egreso", style=BTN_STYLE, command=self._registrar_egreso)\
            .grid(row=1, column=1, pady=10, padx=5)

        # Tabla de estado del día (con cronómetro en curso)
        box = ttk.LabelFrame(self, text="Estado de hoy")
        box.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("empleado", "ingreso", "en_curso", "egreso", "horas")
        self.tree = ttk.Treeview(box, columns=cols, show="headings", height=12)
        headers = ("Empleado", "Ingreso", "En curso", "Egreso", "Horas")
        for c, t in zip(cols, headers):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=140 if c != "empleado" else 200, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    # --------- API que llama el controller ---------
    def mostrar_estado_hoy(self, filas):
        # Limpiar timer previo
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None

        # Re-armar tabla
        self._items_by_emp.clear()
        self._ingresos_str.clear()
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Insertar filas
        for f in filas:
            emp_id = f["empleado_id"]
            ingreso = f["ingreso"] or ""
            egreso = f["egreso"] or ""
            horas = f["horas"] or ""
            en_curso = "" if egreso else "00:00:00"
            item = self.tree.insert("", "end",
                                    values=(f["empleado"], ingreso, en_curso, egreso, horas))
            self._items_by_emp[emp_id] = item
            if not egreso and ingreso:
                self._ingresos_str[emp_id] = ingreso  # guardar para cronómetro

        # Iniciar cronómetro si hay abiertos
        if self._ingresos_str:
            self._tick()

    # --------- Cronómetro: actualiza "En curso" cada 1s ---------
    def _tick(self):
        import datetime as _dt
        for emp_id, item in list(self._items_by_emp.items()):
            if emp_id not in self._ingresos_str:
                continue  # ya cerrado
            ingreso_str = self._ingresos_str[emp_id]
            try:
                h, m, s = [int(p) for p in ingreso_str.split(":")]
                today = _dt.date.today()
                dt_in = _dt.datetime.combine(today, _dt.time(h, m, s))
                elapsed = _dt.datetime.now() - dt_in
                segundos = int(elapsed.total_seconds())
                hh = segundos // 3600
                mm = (segundos % 3600) // 60
                ss = segundos % 60
                en_curso = f"{hh:02d}:{mm:02d}:{ss:02d}"
            except Exception:
                en_curso = ""
            # actualizar columna "en_curso"
            vals = list(self.tree.item(item, "values"))
            if len(vals) >= 5:
                vals[2] = en_curso
                self.tree.item(item, values=vals)

        self._timer_job = self.after(1000, self._tick)

    # --------- Acciones UI ---------
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

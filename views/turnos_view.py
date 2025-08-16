import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta
from controllers.turnos_controller import TurnosController
from ui.ui_theme import COLORS
from tkcalendar import Calendar
import tkinter.simpledialog as simpledialog

class TurnosView(tk.Frame):
    DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

    def __init__(self, parent, on_back=None):
        super().__init__(parent, bg=COLORS.get("bg", "#FFFFFF"))
        self.on_back = on_back
        self.pack(fill="both", expand=True)
        self.controller = TurnosController(self)
        self._build()
        self.controller.cargar_semana()

    def _build(self):
        
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=10, pady=(10, 0))

        ttk.Button(header, text="← Volver", style="Rounded.TButton",
                   command=(self.on_back or (lambda: None))).pack(side="left")

        top = tk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(header, text="📅 Seleccionar fecha", style="Rounded.TButton",
                   command=self._abrir_calendario).pack(side="left", padx=8)

        self.lbl_semana = ttk.Label(header, text="", style="Body.TLabel")
        self.lbl_semana.pack(side="left", padx=12)

        body = tk.Frame(self)
        body.pack(fill="both", expand=True)

        self.grid_frame = tk.Frame(body)
        self.grid_frame.pack(side="left", fill="both", expand=True, padx=(10,5), pady=10)

        self.detail = tk.LabelFrame(body, text="Detalle del turno (n/5)")
        self.detail.pack(side="right", fill="y", padx=(5,10), pady=10)

        self._build_detail()

    def _abrir_calendario(self):
        if Calendar:
            
            top = tk.Toplevel(self)
            top.title("Seleccionar fecha")
            top.resizable(False, False)

            cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
            cal.pack(padx=10, pady=10)

            def usar():
                fecha_sel = cal.get_date()  # 'YYYY-MM-DD'
                self._usar_fecha(fecha_sel)
                top.destroy()

            ttk.Button(top, text="Usar fecha", style="Rounded.TButton", command=usar).pack(pady=(0,10))
        else: 
            # Fallback simple si no está tkcalendar
            fecha_sel = simpledialog.askstring("Fecha", "Ingresá la fecha (YYYY-MM-DD):", parent=self)
            if fecha_sel:
                self._usar_fecha(fecha_sel)

    def _usar_fecha(self, fecha_str: str):
        self.controller.set_fecha_ref(fecha_str)   # actualiza self.ref y recarga semana
        # Actualizar etiqueta de semana
        ini, fin = self.controller.rango_semana_actual()
        self.lbl_semana.config(text=f"Semana: {ini.isoformat()} → {fin.isoformat()}")

    def _build_detail(self):
        f = self.detail
        for w in f.winfo_children():
            w.destroy()
        self.lbl_slot = ttk.Label(f, text="—")
        self.lbl_slot.pack(pady=5)

        self.tree = ttk.Treeview(f, columns=("id", "cliente"), show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.pack(fill="y", padx=10, pady=5)

        frm_add = tk.Frame(f)
        frm_add.pack(fill="x", padx=10, pady=5)
        ttk.Label(frm_add, text="Cliente").grid(row=0, column=0, sticky="w")
        self.cmb_cliente = ttk.Combobox(frm_add, state="readonly", width=28)
        self.cmb_cliente.grid(row=0, column=1, padx=5)

        ttk.Label(frm_add, text="Fecha (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        self.ent_fecha_mov = ttk.Entry(frm_add, width=14)
        self.ent_fecha_mov.grid(row=1, column=1, sticky="w")
        ttk.Label(frm_add, text="Hora (HH:MM:SS)").grid(row=2, column=0, sticky="w")
        self.ent_hora_mov = ttk.Entry(frm_add, width=14)
        self.ent_hora_mov.grid(row=2, column=1, sticky="w")

        btns = tk.Frame(f)
        btns.pack(fill="x", padx=10, pady=5)
        ttk.Button(btns, text="Agregar", command=self._agregar).pack(side="left", padx=3)
        ttk.Button(btns, text="Eliminar", command=self._eliminar).pack(side="left", padx=3)
        ttk.Button(btns, text="Mover", command=self._mover).pack(side="left", padx=3)

    def render_grid(self, ini, fin, horas, counts, max_por_hora):
        self.lbl_semana.config(text=f"Semana: {ini.isoformat()} → {fin.isoformat()}")
        for w in self.grid_frame.winfo_children():
            w.destroy()

        hdr = tk.Frame(self.grid_frame)
        hdr.grid(row=0, column=0, sticky="nsew")
        tk.Label(hdr, text="Hora", bd=1, relief="ridge", width=8).grid(row=0, column=0, sticky="nsew")

        d = ini
        self.fechas_cols = []
        for i, nombre in enumerate(self.DIAS):
            tk.Label(hdr, text=nombre, bd=1, relief="ridge", width=16).grid(row=0, column=i+1, sticky="nsew")
            self.fechas_cols.append(d.isoformat())
            d += timedelta(days=1)

        for r, h in enumerate(horas, start=1):
            tk.Label(self.grid_frame, text=h[:5], bd=1, relief="ridge", width=8).grid(row=r, column=0, sticky="nsew")
            for c, fecha in enumerate(self.fechas_cols, start=1):
                key = (fecha, h)
                n = counts.get(key, 0)
                txt = f"{n}/{max_por_hora}"
                btn = ttk.Button(
                    self.grid_frame,
                    text=txt,
                    width=10,
                    command=lambda f=fecha, hh=h: self.controller.listar_slot(f, hh)
                )
                btn.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")

        # Manejo seguro por si clientes es dict o tupla
        clientes = self.controller.clientes_opciones()
        def formatear_cliente(c):
            if isinstance(c, dict):
                return f"{c.get('id')} - {c.get('nombre','')} {c.get('apellido','')}"
            elif isinstance(c, (list, tuple)) and len(c) >= 3:
                return f"{c[0]} - {c[1]} {c[2]}"
            return ""
        self.cmb_cliente['values'] = [formatear_cliente(c) for c in clientes]


    
    def mostrar_slot(self, fecha, hora, turnos):
        self.lbl_slot.config(text=f"{fecha} {hora[:5]} ( {len(turnos)}/5 )")
        for i in self.tree.get_children():
            self.tree.delete(i)
        for t in turnos:
            if isinstance(t, dict):
                self.tree.insert("", "end", values=(t["id"], f"{t['nombre']} {t['apellido']}"))
            else:
                self.tree.insert("", "end", values=(t[0], f"{t[2]} {t[3]}"))
        self.ent_fecha_mov.delete(0, tk.END); self.ent_fecha_mov.insert(0, fecha)
        self.ent_hora_mov.delete(0, tk.END);  self.ent_hora_mov.insert(0, hora)
        self._slot_activo = (fecha, hora)

    def alerta(self, msg):
        messagebox.showinfo("Aviso", msg)

    def _agregar(self):
        if not hasattr(self, "_slot_activo"):
            self.alerta("Elegí un horario de la grilla")
            return
        sel = self.cmb_cliente.get()
        if not sel:
            self.alerta("Seleccioná un cliente")
            return
        cliente_id = int(sel.split(" - ")[0])
        fecha, hora = self._slot_activo
        self.controller.crear_turno(cliente_id, fecha, hora)

    def _eliminar(self):
        if not hasattr(self, "_slot_activo"):
            self.alerta("Elegí un horario de la grilla")
            return
        item = self.tree.focus()
        if not item:
            self.alerta("Seleccioná un turno en la lista")
            return
        turno_id = int(self.tree.item(item, "values")[0])
        fecha, hora = self._slot_activo
        self.controller.eliminar_turno(turno_id, fecha, hora)

    def _mover(self):
        if not hasattr(self, "_slot_activo"):
            self.alerta("Elegí un horario de la grilla")
            return
        item = self.tree.focus()
        if not item:
            self.alerta("Seleccioná un turno en la lista")
            return
        turno_id = int(self.tree.item(item, "values")[0])
        nueva_fecha = self.ent_fecha_mov.get().strip()
        nueva_hora = self.ent_hora_mov.get().strip() or "07:00:00"
        self.controller.mover_turno(turno_id, nueva_fecha, nueva_hora)

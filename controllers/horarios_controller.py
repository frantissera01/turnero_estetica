# controllers/horarios_controller.py
from datetime import datetime, date, time
from models.horarios_model import HorariosModel
from models.empleados_model import EmpleadosModel

class HorariosController:
    def __init__(self, view):
        self.view = view
        self.model = HorariosModel()
        self.empleados_model = EmpleadosModel()

    def lista_empleados(self):
        return self.empleados_model.obtener_empleados()

    def _fmt_time(self, t):
        if isinstance(t, time):
            return t.strftime("%H:%M:%S")
        try:
            # a veces puede venir como str o Decimal
            s = str(t)
            if len(s) >= 5 and s.count(":") >= 1:
                parts = s.split(":") + ["0","0"]
                h, m, s2 = parts[0:3]
                return f"{int(h):02d}:{int(m):02d}:{int(float(s2)):02d}"
            return s
        except Exception:
            return ""

    def _fmt_hours(self, h):
        try:
            return f"{float(h):.2f}"
        except Exception:
            return "0.00"

    # ---------- acciones ----------
    def registrar_ingreso(self, empleado_id):
        estado = self.model.estado_hoy()
        # Si ya tiene abierto hoy, evitamos duplicar
        for r in estado:
            eid = r["empleado_id"] if isinstance(r, dict) else r[1]
            hora_egreso = r["hora_egreso"] if isinstance(r, dict) else r[3]
            if eid == empleado_id and not hora_egreso:
                self.view.alerta("Este empleado ya tiene un ingreso abierto hoy.")
                self.cargar_estado_hoy()
                return
        self.model.registrar_ingreso(empleado_id)
        self.view.alerta("Ingreso registrado.")
        self.cargar_estado_hoy()

    def registrar_egreso(self, empleado_id):
        data = self.model.registrar_egreso(empleado_id)
        if not data:
            self.view.alerta("No hay ingreso pendiente para este empleado.")
        else:
            msg = (f"Egreso registrado.\n"
                   f"Ingreso: {self._fmt_time(data['hora_ingreso'])}\n"
                   f"Egreso:  {self._fmt_time(data['hora_egreso'])}\n"
                   f"Horas:   {self._fmt_hours(data['horas_trabajadas'])}")
            self.view.alerta(msg)
        self.cargar_estado_hoy()

    def cargar_estado_hoy(self):
        rows = self.model.estado_hoy()
        data = []
        for r in rows:
            if isinstance(r, dict):
                _id = r["id"]; empleado_id = r["empleado_id"]
                ing = self._fmt_time(r["hora_ingreso"])
                egr = self._fmt_time(r["hora_egreso"]) if r["hora_egreso"] else ""
                horas = self._fmt_hours(r["horas_trabajadas"]) if r["horas_trabajadas"] else ""
                nom = f"{r['nombre']} {r['apellido']}"
            else:
                _id = r[0]; empleado_id = r[1]
                ing = self._fmt_time(r[2])
                egr = self._fmt_time(r[3]) if r[3] else ""
                horas = self._fmt_hours(r[4]) if r[4] else ""
                nom = f"{r[5]} {r[6]}"
            data.append({
                "row_id": _id,
                "empleado_id": empleado_id,
                "empleado": nom,
                "ingreso": ing,
                "egreso": egr,
                "horas": horas
            })
        self.view.mostrar_estado_hoy(data)

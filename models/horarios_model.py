# models/horarios_model.py
from models.base_model import BaseModel
from datetime import datetime, date
from utils.conversions import to_time 
 
class HorariosModel(BaseModel):
    def registrar_ingreso(self, empleado_id):
        f = date.today()
        h = datetime.now().time()
        self.execute_query(
            "INSERT INTO horarios_empleados (empleado_id, fecha, hora_ingreso) VALUES (%s, %s, %s)",
            (empleado_id, f, h)
        )

    def registrar_egreso(self, empleado_id):
        f = date.today()
        h_egreso = datetime.now().time()
        reg = self.fetch_one(
            "SELECT id, hora_ingreso FROM horarios_empleados "
            "WHERE empleado_id=%s AND fecha=%s AND hora_egreso IS NULL "
            "ORDER BY id DESC LIMIT 1",
            (empleado_id, f)
        )
        if not reg:
            return None

        hora_ingreso = reg["hora_ingreso"] if isinstance(reg, dict) else reg[1]
        # convertir a datetime para calcular
        dt_in = datetime.combine(f, hora_ingreso)
        dt_out = datetime.combine(f, h_egreso)
        horas = (dt_out - dt_in).total_seconds() / 3600.0

        # tarifa opcional (si la tenés)
        # trow = self.fetch_one("SELECT tarifa_hora FROM empleados WHERE id=%s", (empleado_id,))
        # tarifa = float(trow["tarifa_hora"]) if isinstance(trow, dict) else float(trow[0])
        # pago = horas * tarifa

        self.execute_query(
            "UPDATE horarios_empleados SET hora_egreso=%s, horas_trabajadas=%s WHERE id=%s",
            (h_egreso, horas, reg["id"] if isinstance(reg, dict) else reg[0])
        )
        return {
            "hora_ingreso": hora_ingreso,
            "hora_egreso": h_egreso,
            "horas_trabajadas": horas
        }

    def estado_hoy(self):
        """Devuelve lista de registros de hoy (abiertos y cerrados) con datos de empleado."""
        f = date.today()
        rows = self.fetch_all(
            "SELECT he.id, he.empleado_id, he.hora_ingreso, he.hora_egreso, he.horas_trabajadas, "
            "e.nombre, e.apellido "
            "FROM horarios_empleados he "
            "JOIN empleados e ON e.id = he.empleado_id "
            "WHERE he.fecha=%s "
            "ORDER BY he.hora_ingreso ASC, he.id ASC",
            (f,)
        )
        return rows

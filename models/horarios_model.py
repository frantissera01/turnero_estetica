# models/horarios_model.py
from models.base_model import BaseModel
from datetime import datetime, date
from utils.conversions import to_time 
from typing import Optional, Dict, Any, Union, Tuple

Row = Union[Dict[str, Any], Tuple[Any, ...]]

class HorariosModel(BaseModel):
    def registrar_ingreso(self, empleado_id):
        f = date.today()
        h = datetime.now().time()
        self.execute_query(
            "INSERT INTO horarios_empleados (empleado_id, fecha, hora_ingreso) VALUES (%s, %s, %s)",
            (empleado_id, f, h)
        )

    def registrar_egreso(self, empleado_id: int):
        f = date.today()
        h_egreso = datetime.now().time()
        reg: Optional[Row] = self.fetch_one(
            "SELECT id, hora_ingreso FROM horarios_empleados "
            "WHERE empleado_id=%s AND fecha=%s AND hora_egreso IS NULL "
            "ORDER BY id DESC LIMIT 1",
            (empleado_id, f)
        )
        if not reg:
            return None

        # id y hora_ingreso según dict/tupla
        if isinstance(reg, dict):
            reg_id = reg["id"]
            hora_ingreso_raw = reg["hora_ingreso"]
        else:
            reg_id = reg[0]
            hora_ingreso_raw = reg[1]

        # normalizar hora de ingreso a time
        hi = to_time(hora_ingreso_raw)
        if hi is None:
            # no podemos calcular horas sin una hora válida
            return None

        # calcular horas trabajadas
        dt_in = datetime.combine(f, hi)
        dt_out = datetime.combine(f, h_egreso)
        horas = (dt_out - dt_in).total_seconds() / 3600.0

        self.execute_query(
            "UPDATE horarios_empleados SET hora_egreso=%s, horas_trabajadas=%s WHERE id=%s",
            (h_egreso, horas, reg_id)
        )
        return {
            "hora_ingreso": hi,
            "hora_egreso": h_egreso,
            "horas_trabajadas": horas,
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

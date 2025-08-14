from models.base_model import BaseModel
from decimal import Decimal
from datetime import datetime, time

class HorariosModel(BaseModel):
    def registrar_ingreso(self, empleado_id):
        fecha = datetime.now().date()
        hora = datetime.now().time()
        self.execute_query(
            "INSERT INTO horarios_empleados (empleado_id, fecha, hora_ingreso) VALUES (%s, %s, %s)",
            (empleado_id, fecha, hora)
        )

    def registrar_egreso(self, empleado_id):
        fecha = datetime.now().date()
        hora_egreso = datetime.now().time()

        # Buscar registro de hoy sin hora_egreso
        reg = self.fetch_one(
            "SELECT id, hora_ingreso FROM horarios_empleados WHERE empleado_id=%s AND fecha=%s AND hora_egreso IS NULL",
            (empleado_id, fecha)
        )

        if not isinstance(reg, dict):
            return None, None

        # Convertir hora_ingreso a datetime.time si es necesario
        hora_ingreso_val = reg.get("hora_ingreso")
        if isinstance(hora_ingreso_val, Decimal) or isinstance(hora_ingreso_val, str):
            # Si viene como "HH:MM:SS" o decimal, convertirlo
            hora_ingreso = datetime.strptime(str(hora_ingreso_val), "%H:%M:%S").time()
        elif isinstance(hora_ingreso_val, time):
            hora_ingreso = hora_ingreso_val
        else:
            return None, None

        horas_trab = (
            datetime.combine(fecha, hora_egreso) - datetime.combine(fecha, hora_ingreso)
        ).seconds / 3600.0

        # Obtener tarifa por hora
        tarifa_row = self.fetch_one("SELECT tarifa_hora FROM empleados WHERE id=%s", (empleado_id,))
        if not isinstance(tarifa_row, dict):
            return None, None

        tarifa_val = tarifa_row.get("tarifa_hora")
        if isinstance(tarifa_val, Decimal):
            tarifa = float(tarifa_val)
        elif isinstance(tarifa_val, (int, float)):
            tarifa = tarifa_val
        else:
            return None, None

        pago = horas_trab * tarifa

        self.execute_query(
            "UPDATE horarios_empleados SET hora_egreso=%s, horas_trabajadas=%s, pago_diario=%s WHERE id=%s",
            (hora_egreso, horas_trab, pago, reg.get("id"))
        )
        return horas_trab, pago


    def estado_actual(self, empleado_id):
        fecha = datetime.now().date()
        reg = self.fetch_one(
            "SELECT hora_ingreso, hora_egreso FROM horarios_empleados WHERE empleado_id=%s AND fecha=%s ORDER BY id DESC LIMIT 1",
            (empleado_id, fecha)
        )
        return reg

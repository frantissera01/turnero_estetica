from models.base_model import BaseModel
from typing import Any, Dict, Tuple, Union
from datetime import datetime

Row = Union[Dict[str, object], Tuple[object, ...]]

class EmpleadosModel(BaseModel):
    def obtener_empleados(self):
        return self.fetch_all("SELECT * FROM empleados ORDER BY id DESC")

    def agregar_empleado(self, nombre, apellido, tarifa):
        self.execute_query(
            "INSERT INTO empleados (nombre, apellido, tarifa_hora) VALUES (%s, %s, %s)",
            (nombre, apellido, tarifa)
        )

    def actualizar_empleado(self, empleado_id, nombre, apellido, tarifa):
        self.execute_query(
            "UPDATE empleados SET nombre=%s, apellido=%s, tarifa_hora=%s WHERE id=%s",
            (nombre, apellido, tarifa, empleado_id)
        )

    def eliminar_empleado(self, empleado_id):
        self.execute_query("DELETE FROM empleados WHERE id = %s", (empleado_id,))

    def listar_saldos_pendientes(self):
        """
        Devuelve: id, nombre, apellido, devengado, pagado, saldo
        """
        q = """
        SELECT e.id,
               e.nombre,
               e.apellido,
               COALESCE(SUM(he.pago_diario), 0) AS devengado,
               COALESCE((SELECT SUM(p.monto) FROM pagos_empleados p WHERE p.empleado_id = e.id), 0) AS pagado,
               (COALESCE(SUM(he.pago_diario), 0) - COALESCE((SELECT SUM(p.monto) FROM pagos_empleados p WHERE p.empleado_id = e.id), 0)) AS saldo
          FROM empleados e
          LEFT JOIN horarios_empleados he ON he.empleado_id = e.id
         GROUP BY e.id, e.nombre, e.apellido
        HAVING saldo > 0
         ORDER BY saldo DESC, e.apellido, e.nombre
        """
        return self.fetch_all(q)

    def registrar_pago(self, empleado_id: int, monto: float, observacion: str = ""):
        now = datetime.now()
        self.execute_query(
            "INSERT INTO pagos_empleados (empleado_id, fecha, monto, observacion) VALUES (%s, %s, %s, %s)",
            (empleado_id, now, monto, observacion)
        )

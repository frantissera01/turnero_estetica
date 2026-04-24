from models.base_model import BaseModel
from typing import Dict, Tuple, Union
from typing import Any

Row = Union[Dict[str, Any], Tuple[Any, ...], None]

class PlanesModel(BaseModel):

    def safe_int(x: Any, default: int = 0) -> int:
        if x is None:
            return default
        try:
            return int(x)
        except Exception:
            try:
                return int(str(x))
            except Exception:
                return default
        
    # ---------- CRUD PLANES ----------
    def listar_planes(self):
        return self.fetch_all(
            "SELECT id, nombre, descripcion, total_sesiones, precio FROM planes ORDER BY id DESC"
        )

    def crear_plan(self, nombre, descripcion, total_sesiones, precio):
        self.execute_query(
            "INSERT INTO planes (nombre, descripcion, total_sesiones, precio) VALUES (%s, %s, %s, %s)",
            (nombre, descripcion, total_sesiones, precio)
        )

    def actualizar_plan(self, plan_id, nombre, descripcion, total_sesiones, precio):
        self.execute_query(
            "UPDATE planes SET nombre=%s, descripcion=%s, total_sesiones=%s, precio=%s WHERE id=%s",
            (nombre, descripcion, total_sesiones, precio, plan_id)
        )

    def eliminar_plan(self, plan_id):
        # Nota: podrías impedir borrar si está asignado; aquí lo permitimos y confiamos en FK.
        self.execute_query("DELETE FROM planes WHERE id=%s", (plan_id,))

    # ---------- CLIENTES Y ASIGNACIONES ----------
    def listar_clientes(self):
        # Devuelve id, nombre, apellido
        return self.fetch_all(
            "SELECT id, nombre, apellido FROM clientes ORDER BY apellido, nombre"
        )

    def listar_asignaciones(self):
        # Lista todas las asignaciones con sesiones usadas/restantes
        return self.fetch_all(
            """
            SELECT cp.id, cp.cliente_id, cp.plan_id, cp.fecha_inicio, cp.sesiones_usadas,
                   c.nombre AS c_nombre, c.apellido AS c_apellido,
                   p.nombre AS p_nombre, p.total_sesiones
              FROM clientes_planes cp
              JOIN clientes c ON c.id = cp.cliente_id
              JOIN planes p   ON p.id = cp.plan_id
             ORDER BY cp.id DESC
            """
        )

    def asignar_plan(self, cliente_id, plan_id, fecha_inicio):
        self.execute_query(
            "INSERT INTO clientes_planes (cliente_id, plan_id, fecha_inicio, sesiones_usadas) VALUES (%s, %s, %s, 0)",
            (cliente_id, plan_id, fecha_inicio)
        )

    def eliminar_asignacion(self, asignacion_id):
        self.execute_query("DELETE FROM clientes_planes WHERE id=%s", (asignacion_id,))

    def obtener_totales_plan(self, plan_id: int) -> int:
        row: Row = self.fetch_one(
            "SELECT total_sesiones FROM planes WHERE id=%s",
            (plan_id,)
        )
        if not row:
            return 0
        if isinstance(row, dict):
            val = row["total_sesiones"] if "total_sesiones" in row else 0
            return self.safe_int(val)
        # rama tupla
        return self.safe_int(row[0])

    def marcar_sesion_usada(self, asignacion_id: int):
        row: Row = self.fetch_one(
            """
            SELECT cp.sesiones_usadas, p.total_sesiones
              FROM clientes_planes cp
              JOIN planes p ON p.id = cp.plan_id
             WHERE cp.id=%s
            """,
            (asignacion_id,)
        )
        if not row:
            return False, "Asignación no encontrada"

        if isinstance(row, dict):
            usadas_raw = row["sesiones_usadas"] if "sesiones_usadas" in row else 0
            total_raw  = row["total_sesiones"]   if "total_sesiones"   in row else 0
        else:
            # tupla: (0)=usadas, (1)=total
            usadas_raw = row[0]
            total_raw  = row[1]

        usadas = self.safe_int(usadas_raw)
        total  = self.safe_int(total_raw)

        if usadas >= total:
            return False, "No quedan sesiones disponibles"

        self.execute_query(
            "UPDATE clientes_planes SET sesiones_usadas = sesiones_usadas + 1 WHERE id=%s",
            (asignacion_id,)
        )
        return True, "Sesión marcada"

    def marcar_sesion_revertir(self, asignacion_id: int):
        row: Row = self.fetch_one(
            "SELECT sesiones_usadas FROM clientes_planes WHERE id=%s",
            (asignacion_id,)
        )
        if not row:
            return False, "Asignación no encontrada"

        if isinstance(row, dict):
            usadas_raw = row["sesiones_usadas"] if "sesiones_usadas" in row else 0
        else:
            # tupla: (0)=usadas
            usadas_raw = row[0]

        usadas = self.safe_int(usadas_raw)
        if usadas <= 0:
            return False, "No hay sesiones para revertir"

        self.execute_query(
            "UPDATE clientes_planes SET sesiones_usadas = sesiones_usadas - 1 WHERE id=%s",
            (asignacion_id,)
        )
        return True, "Sesión revertida"
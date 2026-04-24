from models.base_model import BaseModel

class TurnosModel(BaseModel):
    MAX_POR_HORA = 5

    def turnos_de_semana(self, fecha_inicio, fecha_fin):
        return self.fetch_all(
            """
            SELECT t.id, t.cliente_id, t.fecha, t.hora,
                   c.nombre, c.apellido
              FROM turnos t
              JOIN clientes c ON c.id = t.cliente_id
             WHERE t.fecha BETWEEN %s AND %s
             ORDER BY t.fecha, t.hora
            """,
            (fecha_inicio, fecha_fin)
        )

    def contar_por_slot(self, fecha_inicio, fecha_fin):
        return self.fetch_all(
            """
            SELECT fecha, hora, COUNT(*) AS cantidad
              FROM turnos
             WHERE fecha BETWEEN %s AND %s
             GROUP BY fecha, hora
            """,
            (fecha_inicio, fecha_fin)
        )

    def listar_slot(self, fecha, hora):
        return self.fetch_all(
            """
            SELECT t.id, t.cliente_id, c.nombre, c.apellido
              FROM turnos t
              JOIN clientes c ON c.id = t.cliente_id
             WHERE t.fecha=%s AND t.hora=%s
             ORDER BY t.id DESC
            """,
            (fecha, hora)
        )

    def crear(self, cliente_id, fecha, hora):
        self.execute_query(
            "INSERT INTO turnos (cliente_id, fecha, hora) VALUES (%s, %s, %s)",
            (cliente_id, fecha, hora)
        )

    def mover(self, turno_id, nueva_fecha, nueva_hora):
        self.execute_query(
            "UPDATE turnos SET fecha=%s, hora=%s WHERE id=%s",
            (nueva_fecha, nueva_hora, turno_id)
        )

    def eliminar(self, turno_id):
        self.execute_query("DELETE FROM turnos WHERE id=%s", (turno_id,))

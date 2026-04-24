from models.base_model import BaseModel

class ClientesModel(BaseModel):
    def obtener_clientes(self):
        return self.fetch_all("SELECT * FROM clientes ORDER BY id DESC")

    def agregar_cliente(self, nombre, apellido, telefono, documento, sesiones_restantes, estado_pago):
        self.execute_query(
            """
            INSERT INTO clientes (nombre, apellido, telefono, documento, sesiones_restantes, estado_pago)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nombre, apellido, telefono, documento, sesiones_restantes, estado_pago)
        )

    def actualizar_cliente(self, cliente_id, nombre, apellido, telefono, documento, sesiones_restantes, estado_pago):
        self.execute_query(
            """
            UPDATE clientes
               SET nombre=%s, apellido=%s, telefono=%s, documento=%s, sesiones_restantes=%s, estado_pago=%s
             WHERE id=%s
            """,
            (nombre, apellido, telefono, documento, sesiones_restantes, estado_pago, cliente_id)
        )

    def eliminar_cliente(self, cliente_id):
        self.execute_query("DELETE FROM clientes WHERE id=%s", (cliente_id,))

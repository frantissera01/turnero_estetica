from models.base_model import BaseModel

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

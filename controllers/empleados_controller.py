from models.empleados_model import EmpleadosModel

class EmpleadosController:
    def __init__(self, view):
        self.view = view
        self.model = EmpleadosModel()

    def cargar_empleados(self):
        empleados = self.model.obtener_empleados()
        self.view.mostrar_empleados(empleados)

    def guardar(self, datos):
        eid = datos.get("id")
        if eid:
            self.model.actualizar_empleado(eid, datos["nombre"], datos["apellido"], datos["tarifa"]) 
        else:
            self.model.agregar_empleado(datos["nombre"], datos["apellido"], datos["tarifa"]) 
        self.cargar_empleados()

    def eliminar(self, empleado_id):
        self.model.eliminar_empleado(empleado_id)
        self.cargar_empleados()

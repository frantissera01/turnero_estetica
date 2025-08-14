from models.horarios_model import HorariosModel
from models.empleados_model import EmpleadosModel

class HorariosController:
    def __init__(self, view):
        self.view = view
        self.model = HorariosModel()
        self.empleados_model = EmpleadosModel()

    def lista_empleados(self):
        return self.empleados_model.obtener_empleados()

    def registrar_ingreso(self, empleado_id):
        estado = self.model.estado_actual(empleado_id)
        if isinstance(estado, dict) and not estado.get("hora_egreso"):
            self.view.alerta("Este empleado ya tiene un ingreso registrado hoy.")
            return
        self.model.registrar_ingreso(empleado_id)
        self.view.alerta("Ingreso registrado.")

    def registrar_egreso(self, empleado_id):
        estado = self.model.estado_actual(empleado_id)
        if not isinstance(estado, dict) or estado.get("hora_egreso"):
            self.view.alerta("Este empleado no tiene ingreso pendiente de egreso hoy.")
            return
        horas, pago = self.model.registrar_egreso(empleado_id)
        if horas is not None:
            self.view.alerta(f"Egreso registrado. Horas: {horas:.2f}, Pago: ${pago:.2f}")

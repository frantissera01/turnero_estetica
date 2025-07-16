# controllers/empleados_controller.py
from models.empleados_model import(
    insertar_empleado,
    obtener_empleados_activos,
    baja_empleado,
) 
from models.empleados_model import obtener_empleados_inactivos, reactivar_empleado as reactivar

def registrar_empleado(nombre, tarifa):
    return insertar_empleado(nombre, tarifa)

def listar_empleados():
    return obtener_empleados_activos()

def eliminar_empleado(empleado_id):
    baja_empleado(empleado_id)


def listar_empleados_inactivos():
    return obtener_empleados_inactivos()

def reactivar_empleado(empleado_id):
    reactivar(empleado_id)


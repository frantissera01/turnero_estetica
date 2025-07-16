# controllers/planes_controller.py

from models.planes_model import crear_plan, obtener_planes, eliminar_plan

def registrar_plan(nombre, descripcion, precio, sesiones):
    crear_plan(nombre, descripcion, precio, sesiones)

def listar_planes():
    return obtener_planes()

def borrar_plan(plan_id):
    eliminar_plan(plan_id)

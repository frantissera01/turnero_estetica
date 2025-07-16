
from models.turnos_model import (
    agregar_turno,
    eliminar_turno,
    obtener_turnos_por_fecha_y_hora,
    listar_turnos as listar_turnos_con_cliente
)

def listar_turnos(fecha, hora):
    return listar_turnos_con_cliente(fecha, hora)

def registrar_turno(cliente_id, fecha, hora):
    turnos = obtener_turnos_por_fecha_y_hora(fecha, hora)
    if len(turnos) >= 5:
        raise Exception("No se pueden registrar más de 5 clientas en este horario.")
    agregar_turno(cliente_id, fecha, hora)

def borrar_turno_controller(turno_id):
    eliminar_turno(turno_id)


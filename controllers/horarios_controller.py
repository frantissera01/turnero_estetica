from models.horarios_model import (
    insertar_ingreso,
    actualizar_egreso,
    obtener_registro_sin_egreso,
    empleados_disponibles_para_ingreso,
    calcular_horas_y_monto
)
from models.empleados_model import obtener_empleado_por_id
from datetime import datetime, time, timedelta


def registrar_ingreso(empleado_id):
    ahora = datetime.now()
    insertar_ingreso(empleado_id, ahora.date(), ahora.time())

def registrar_egreso(empleado_id):
    ahora = datetime.now()
    registro = obtener_registro_sin_egreso(empleado_id)

    if not registro:
        return

    hora_raw = registro["hora_ingreso"]
    fecha = registro["fecha"]

    # Convertimos hora_ingreso a datetime
    if isinstance(hora_raw, timedelta):
        total_segundos = int(hora_raw.total_seconds())
        hora_convertida = time(
            hour=total_segundos // 3600,
            minute=(total_segundos % 3600) // 60,
            second=total_segundos % 60
        )
        hora_ingreso_str = hora_convertida.strftime("%H:%M:%S")

    elif isinstance(hora_raw, time):
        hora_ingreso_str = hora_raw.strftime("%H:%M:%S")

    elif isinstance(hora_raw, str):
        hora_ingreso_str = hora_raw

    else:
        raise Exception(f"Formato no reconocido para hora_ingreso: {type(hora_raw)}")

    hora_egreso_str = ahora.strftime("%H:%M:%S")

    tarifa = float(registro["tarifa_por_hora"])
    horas_trabajadas, monto_dia= calcular_horas_y_monto(hora_ingreso_str, hora_egreso_str, tarifa)

    actualizar_egreso(
        empleado_id,
        ahora.time(),
        round(horas_trabajadas, 2),
        round(monto_dia, 2)
    )

def listar_empleados_disponibles():
    return empleados_disponibles_para_ingreso()

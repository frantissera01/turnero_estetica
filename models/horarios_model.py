from models.db import conectar
from datetime import datetime
from typing import Any, Tuple


def insertar_ingreso(empleado_id, fecha, hora_ingreso):
    conn = conectar()
    cursor = conn.cursor()
    query = """
        INSERT INTO horarios (empleado_id, fecha, hora_ingreso)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (empleado_id, fecha, hora_ingreso))
    conn.commit()
    conn.close()


def obtener_registro_sin_egreso(empleado_id) -> Any:
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT h.id, h.fecha, h.hora_ingreso, e.tarifa_por_hora
        FROM horarios h
        JOIN empleados e ON h.empleado_id = e.id
        WHERE h.empleado_id = %s AND h.hora_egreso IS NULL
        ORDER BY h.id DESC
        LIMIT 1
    """
    cursor.execute(query, (empleado_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def calcular_horas_y_monto(hora_ingreso: str, hora_egreso: str, tarifa_por_hora: float) -> Tuple[float, float]:
    fmt = "%H:%M:%S"  # formato esperado, ajustar si usás otro
    ingreso_dt = datetime.strptime(hora_ingreso, fmt)
    egreso_dt = datetime.strptime(hora_egreso, fmt)

    delta = egreso_dt - ingreso_dt
    horas = delta.total_seconds() / 3600

    monto_dia = round(horas * tarifa_por_hora, 2)
    return horas, monto_dia


def actualizar_egreso(empleado_id, hora_egreso, horas_trabajadas, monto_dia):
    conn = conectar()
    cursor = conn.cursor()
    query = """
        UPDATE horarios
        SET hora_egreso = %s,
            horas_trabajadas = %s,
            monto_dia = %s
        WHERE empleado_id = %s AND hora_egreso IS NULL
    """
    cursor.execute(query, (hora_egreso, horas_trabajadas, monto_dia, empleado_id))
    conn.commit()
    conn.close()


def empleados_en_turno():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT e.id, e.nombre
        FROM horarios h
        JOIN empleados e ON h.empleado_id = e.id
        WHERE h.hora_egreso IS NULL AND e.activo = TRUE
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def empleados_disponibles_para_ingreso():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT e.id, e.nombre
        FROM empleados e
        WHERE e.activo = TRUE
        AND e.id NOT IN (
            SELECT empleado_id
            FROM horarios
            WHERE hora_ingreso IS NOT NULL AND hora_egreso IS NULL
        )
    """

    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

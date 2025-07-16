from models.db import conectar
from typing import Any
from datetime import date

def obtener_historial_empleado(empleado_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT fecha, horas_trabajadas, monto_dia
        FROM horarios
        WHERE empleado_id = %s AND hora_egreso IS NOT NULL
        ORDER BY fecha DESC
    """
    cursor.execute(query, (empleado_id,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado


def obtener_total_a_cobrar(empleado_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # Buscar fecha del último pago
    cursor.execute("""
        SELECT fecha_pago 
        FROM pagos 
        WHERE empleado_id = %s 
        ORDER BY fecha_pago DESC 
        LIMIT 1
    """, (empleado_id,))
    resultado = cursor.fetchone()
    resultado: Any
    ultima_fecha_pago = resultado["fecha_pago"] if resultado else date(2000, 1, 1)  # fecha muy antigua si nunca se pagó

    # Sumar lo trabajado desde entonces hasta hoy
    cursor.execute("""
        SELECT SUM(monto_dia) AS total
        FROM horarios
        WHERE empleado_id = %s AND hora_egreso IS NOT NULL AND fecha > %s
    """, (empleado_id, ultima_fecha_pago))
    resultado = cursor.fetchone()
    return resultado["total"] or 0.0


def obtener_total_pagado(empleado_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT SUM(monto_pagado) AS total
        FROM pagos
        WHERE empleado_id = %s
    """
    cursor.execute(query, (empleado_id,))
    resultado = cursor.fetchone()
    resultado:Any
    return resultado["total"] or 0.0


def registrar_pago(empleado_id, monto_pagado):
    conn = conectar()
    cursor = conn.cursor()
    query = """
        INSERT INTO pagos (empleado_id, fecha_pago, monto_pagado)
        VALUES (%s, CURDATE(), %s)
    """
    cursor.execute(query, (empleado_id, monto_pagado))
    conn.commit()


def obtener_ultimo_pago(empleado_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT fecha_pago, monto_pagado
        FROM pagos
        WHERE empleado_id = %s
        ORDER BY fecha_pago DESC
        LIMIT 1
    """
    cursor.execute(query, (empleado_id,))
    resultado = cursor.fetchone()
    resultado:Any
    if resultado:
        return {
            "fecha": resultado["fecha_pago"],
            "monto": resultado["monto_pagado"]
        }
    else:
        return {
            "fecha": "Nunca",
            "monto": 0.0
        }

from models.db import conectar
from datetime import date
from typing import Any

def registrar_pago_manual(empleado_id: int, monto: float):
    conn = conectar()
    cursor = conn.cursor()

    hoy = date.today()
    query = """
        INSERT INTO pagos (empleado_id, fecha_pago, monto_pagado)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (empleado_id, hoy, monto))
    conn.commit()
    conn.close()

def obtener_total_pagado(empleado_id: int) -> float:
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT SUM(monto_pagado) AS total_pagado
        FROM pagos
        WHERE empleado_id = %s
    """
    cursor.execute(query, (empleado_id,))
    resultado = cursor.fetchone()
    conn.close()
    resultado:Any

    if resultado and resultado["total_pagado"]:
        return float(resultado["total_pagado"])
    return 0.0

def obtener_ultimo_pago(empleado_id: int) -> Any:
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
    conn.close()
    resultado:Any
    if resultado:
        return {
            "fecha": resultado["fecha_pago"],
            "monto": resultado["monto_pagado"]
        }
    else:
        return None

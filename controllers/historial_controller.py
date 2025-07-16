from models.historial_model import obtener_historial_empleado
from models.empleados_model import obtener_empleado_por_id
from models.pagos_model import (
    registrar_pago_manual,
    obtener_total_pagado,
    obtener_ultimo_pago
)
from typing import Any

def obtener_perfil_empleado(empleado_id):
   historial = obtener_historial_empleado(empleado_id)
   total_generado = 0.0
   r:Any
   for r in historial:
        if "monto_dia" in r and isinstance(r["monto_dia"], (int, float)):
            total_generado += float(r["monto_dia"])


   total_pagado = obtener_total_pagado(empleado_id)
   ultimo_pago = obtener_ultimo_pago(empleado_id)

   empleado = obtener_empleado_por_id(empleado_id)
   empleado:Any

   return {
        "nombre": empleado["nombre"],
        "tarifa": empleado["tarifa_por_hora"],
        "historial": historial,
        "total_a_cobrar": round(total_generado - total_pagado, 2),
        "total_pagado": round(total_pagado, 2),
        "ultimo_pago": ultimo_pago
    }

def abonar_empleado(empleado_id: int , monto_pagado: float):
    registrar_pago_manual(empleado_id, monto_pagado)


# controllers/clientes_controller.py
from models.cliente_model import (
    crear_cliente,
    obtener_clientes,
    conectar,
    eliminar_cliente,
    actualizar_datos_basicos  # Usamos esta para nombre y teléfono
)

def registrar_cliente(nombre, dni_3, telefono):
    if len(dni_3) != 3 or not dni_3.isdigit():
        raise ValueError("DNI inválido (deben ser 3 dígitos)")
    crear_cliente(nombre, dni_3, telefono)

def listar_clientes():
    return obtener_clientes()

def actualizar_cliente(cliente_id, nombre, telefono):
    actualizar_datos_basicos(cliente_id, nombre, telefono)

def borrar_cliente(cliente_id):
    eliminar_cliente(cliente_id)

def listar_clientes_por_dni(dni_ultimos3):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM clientes WHERE dni_ultimos3 = %s"
    cursor.execute(query, (dni_ultimos3,))
    return cursor.fetchall()

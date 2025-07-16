# models/empleados_model.py
from models.db import conectar


def insertar_empleado(nombre, tarifa_por_hora):
    conn = conectar()
    cursor = conn.cursor()
    query = "INSERT INTO empleados (nombre, tarifa_por_hora) VALUES (%s, %s)"
    cursor.execute(query, (nombre, tarifa_por_hora))
    conn.commit()
    conn.close()

def obtener_empleados_activos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, nombre, tarifa_por_hora FROM empleados WHERE activo = TRUE"
    cursor.execute(query)
    return cursor.fetchall()

def obtener_empleado_por_id(empleado_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query="SELECT id, nombre, tarifa_por_hora  FROM empleados WHERE id = %s"
    cursor.execute(query, (empleado_id,))
    empleado = cursor.fetchone()
    conn.close()
    return empleado

def baja_empleado(empleado_id):
    conn = conectar()
    cursor = conn.cursor()
    query = "UPDATE empleados SET activo = FALSE WHERE id = %s"
    cursor.execute(query, (empleado_id,))
    conn.commit()

def obtener_empleados_inactivos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, nombre, tarifa_por_hora FROM empleados WHERE activo = FALSE"
    cursor.execute(query)
    return cursor.fetchall()

def reactivar_empleado(empleado_id):
    conn = conectar()
    cursor = conn.cursor()
    query = "UPDATE empleados SET activo = TRUE WHERE id = %s"
    cursor.execute(query, (empleado_id,))
    conn.commit()


# models/planes_model.py

from models.db import conectar

def crear_plan(nombre, descripcion, precio, sesiones):
    conn = conectar()
    cursor = conn.cursor()
    query = """
        INSERT INTO planes (nombre, descripcion, precio, sesiones)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, descripcion, precio, sesiones))
    conn.commit()
    conn.close()

def obtener_planes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM planes"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def eliminar_plan(plan_id):
    conn = conectar()
    cursor = conn.cursor()
    query = "DELETE FROM planes WHERE id = %s"
    cursor.execute(query, (plan_id,))
    conn.commit()
    conn.close()

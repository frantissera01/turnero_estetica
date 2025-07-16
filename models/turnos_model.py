from models.db import conectar

def obtener_turnos_por_fecha_y_hora(fecha, hora):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT id, cliente_id
    FROM turnos
    WHERE fecha = %s AND hora = %s
    """
    cursor.execute(query, (fecha, hora))
    turnos = cursor.fetchall()
    print("DEBUG turnos:", turnos)  
    conn.close()
    return turnos

def agregar_turno(cliente_id, fecha, hora):
    conn = conectar()
    cursor = conn.cursor()
    query = "INSERT INTO turnos (fecha, hora, cliente_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (fecha, hora, cliente_id))
    conn.commit()
    conn.close()

def eliminar_turno(turno_id):
    conn = conectar()
    cursor = conn.cursor()
    query = "DELETE FROM turnos WHERE id = %s"
    cursor.execute(query, (turno_id,))
    conn.commit()
    conn.close()

def listar_turnos(fecha, hora):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT t.id AS turno_id, t.fecha, t.hora, t.cliente_id,
               c.nombre AS nombre_cliente, c.dni_ultimos3
        FROM turnos t
        JOIN clientes c ON t.cliente_id = c.id
        WHERE t.fecha = %s AND t.hora = %s
    """
    cursor.execute(query, (fecha, hora))
    resultados = cursor.fetchall()
    conn.close()
    return resultados


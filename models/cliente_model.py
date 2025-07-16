# models/cliente_model.py
from models.db import conectar

def crear_cliente(nombre, dni_3, telefono, sesion_actual=1, estado_pago="pagado"):
    conn = conectar()
    cursor = conn.cursor()
    query = """
    INSERT INTO clientes (nombre, dni_ultimos3, telefono, sesion_actual, estado_pago)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, dni_3, telefono, sesion_actual, estado_pago))
    conn.commit()
    conn.close()

def obtener_clientes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    print("Clientes desde DB:", clientes)
    conn.close()
    return clientes

def actualizar_datos_basicos(cliente_id, nombre, telefono):
    conn = conectar()
    cursor = conn.cursor()
    query = "UPDATE clientes SET nombre=%s, telefono=%s WHERE id=%s"
    cursor.execute(query, (nombre, telefono, cliente_id))
    conn.commit()
    conn.close()



def actualizar_cliente(cliente_id, nombre, telefono, sesion_actual, estado_pago):
    conn = conectar()
    cursor = conn.cursor()
    query = """
    UPDATE clientes SET nombre=%s, telefono=%s, sesion_actual=%s, estado_pago=%s
    WHERE id=%s
    """
    cursor.execute(query, (nombre, telefono, sesion_actual, estado_pago, cliente_id))
    conn.commit()
    conn.close()

def eliminar_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("DEBUG: Probando obtener_clientes()")
    clientes = obtener_clientes()
    for cliente in clientes:
        print(cliente, type(cliente))

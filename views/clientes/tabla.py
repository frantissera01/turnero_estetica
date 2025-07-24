import tkinter as tk
from typing import Any
from tkinter import messagebox, ttk
from controllers.clientes_controller import listar_clientes, borrar_cliente

def crear_tabla(frame):
    columnas = ("ID", "Nombre", "DNI", "Teléfono", "Sesión", "Estado")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=100)
    tabla.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
    return tabla

def actualizar_tabla(tabla):
    for fila in tabla.get_children():
        tabla.delete(fila)
        cliente: Any
    for cliente in listar_clientes():
        tabla.insert("", "end", values=(
            cliente["id"],
            cliente["nombre"],
            cliente["dni_ultimos3"],
            cliente["telefono"],
            cliente.get("sesion_actual", ""),
            cliente.get("estado_pago", "")
        ))

def eliminar_cliente_seleccionado(tabla, actualizar_tabla_callback):
    seleccion = tabla.selection()
    if seleccion:
        cliente_id = tabla.item(seleccion[0])["values"][0]
        confirmacion = messagebox.askyesno("Confirmar", "¿Eliminar cliente seleccionado?")
        if confirmacion:
            try:
                borrar_cliente(cliente_id)
                actualizar_tabla_callback()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")
    else:
        messagebox.showwarning("Advertencia", "Seleccioná un cliente para eliminar.")

def editar_cliente_seleccionado(tabla, entradas, estado, btn_agregar, actualizar_tabla_callback):
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccioná un cliente para editar.")
        return

    valores = tabla.item(seleccion[0])["values"]

    entradas["nombre"].delete(0, tk.END)
    entradas["dni"].delete(0, tk.END)
    entradas["telefono"].delete(0, tk.END)

    entradas["nombre"].insert(0, valores[1])
    entradas["dni"].insert(0, valores[2])
    entradas["telefono"].insert(0, valores[3])

    estado["cliente_en_edicion"] = valores[0]
    btn_agregar.config(text="Guardar Cambios", command=lambda: guardar_cambios(entradas, estado, actualizar_tabla_callback, btn_agregar))

def guardar_cambios(entradas, estado, actualizar_tabla, btn):
    from .form import guardar_cambios as form_guardar_cambios
    form_guardar_cambios(entradas, estado, actualizar_tabla, btn)

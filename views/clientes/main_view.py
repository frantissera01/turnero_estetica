import tkinter as tk
from tkinter import ttk, messagebox
from .form import crear_formulario, limpiar_formulario, agregar_cliente, guardar_cambios
from .tabla import crear_tabla, actualizar_tabla, eliminar_cliente_seleccionado, editar_cliente_seleccionado

def abrir_clientes(contenedor):
    # Limpiar contenido previo
    for widget in contenedor.winfo_children():
        widget.destroy()

    # Crear frame principal
    frame = tk.Frame(contenedor)
    frame.pack(fill="both", expand=True)

    # Estado global para el cliente en edición
    estado = {"cliente_en_edicion": None}

    # Crear formulario de cliente
    entradas = crear_formulario(frame, estado)

    # Crear botón de acción (Agregar o Guardar)
    btn_agregar = tk.Button(
        frame,
        text="Agregar Cliente",
        command=lambda: agregar_cliente(entradas, estado, actualizar_tabla_wrapper, btn_agregar)
    )
    btn_agregar.grid(row=4, column=1, pady=10)

    # Crear tabla
    tabla = crear_tabla(frame)

    def actualizar_tabla_wrapper():
        actualizar_tabla(tabla)

    # Botones para editar y eliminar
    tk.Button(
        frame,
        text="Eliminar Cliente",
        command=lambda: eliminar_cliente_seleccionado(tabla, actualizar_tabla_wrapper)
    ).grid(row=7, column=1, pady=5)

    tk.Button(
        frame,
        text="Editar Cliente",
        command=lambda: editar_cliente_seleccionado(
            tabla, entradas, estado, btn_agregar, actualizar_tabla
        )
    ).grid(row=8, column=1, pady=5)

    # Cargar datos iniciales
    actualizar_tabla_wrapper()

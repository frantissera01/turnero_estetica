import tkinter as tk
from tkinter import messagebox
from controllers.clientes_controller import registrar_cliente, actualizar_cliente

def solo_numeros(max_len=None):
    def validador(texto):
        if texto.isdigit() or texto == "":
            return len(texto) <= max_len if max_len else True
        return False
    return validador

def crear_formulario(frame, estado):
    # Validaciones
    vcmd_dni = frame.register(solo_numeros(3))
    vcmd_tel = frame.register(solo_numeros(12))

    # Campos
    tk.Label(frame, text="Nombre").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(frame)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="DNI (últimos 3)").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_dni = tk.Entry(frame, validate="key", validatecommand=(vcmd_dni, "%P"))
    entry_dni.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Teléfono").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_telefono = tk.Entry(frame, validate="key", validatecommand=(vcmd_tel, "%P"))
    entry_telefono.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(
        frame,
        text="El número telefónico debe contener entre 7 y 12 dígitos.",
        font=("Arial", 8), fg="gray"
    ).grid(row=3, column=1, sticky="w", padx=10)

    # Retornar las entradas en un diccionario
    return {
        "nombre": entry_nombre,
        "dni": entry_dni,
        "telefono": entry_telefono
    }

def limpiar_formulario(entradas):
    entradas["nombre"].delete(0, tk.END)
    entradas["dni"].delete(0, tk.END)
    entradas["telefono"].delete(0, tk.END)

def agregar_cliente(entradas, estado, actualizar_tabla, btn):
    nombre = entradas["nombre"].get().strip()
    dni = entradas["dni"].get().strip()
    telefono = entradas["telefono"].get().strip()

    if len(telefono) < 7:
        messagebox.showerror("Error", "El número de teléfono debe tener al menos 7 dígitos.")
        return

    try:
        registrar_cliente(nombre, dni, telefono)
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
        limpiar_formulario(entradas)
        actualizar_tabla()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def guardar_cambios(entradas, estado, actualizar_tabla, btn):
    cliente_id = estado.get("cliente_en_edicion")
    if cliente_id is None:
        return

    nombre = entradas["nombre"].get().strip()
    telefono = entradas["telefono"].get().strip()

    if len(telefono) < 7:
        messagebox.showerror("Error", "El número de teléfono debe tener al menos 7 dígitos.")
        return

    try:
        actualizar_cliente(cliente_id, nombre, telefono)
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
        limpiar_formulario(entradas)
        actualizar_tabla()
        btn.config(text="Agregar Cliente", command=lambda: agregar_cliente(entradas, estado, actualizar_tabla, btn))
        estado["cliente_en_edicion"] = None
    except Exception as e:
        messagebox.showerror("Error", str(e))

import tkinter as tk
from tkinter import messagebox, ttk
from controllers.clientes_controller import registrar_cliente, listar_clientes, borrar_cliente, actualizar_cliente
from typing import Any

def abrir_clientes(contenedor):
    for widget in contenedor.winfo_children():
        widget.destroy()
    frame = tk.Frame(contenedor)
    frame.pack(fill="both", expand=True)

    estado = {"cliente_en_edicion": None}

    def solo_numeros(max_len=None):
        def validador(texto):
            if texto.isdigit() or texto == "":
                return len(texto) <= max_len if max_len else True
            return False
        return validador

    vcmd_dni = frame.register(solo_numeros(3))
    vcmd_tel = frame.register(solo_numeros(12))

    tk.Label(frame, text="Nombre").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(frame)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="DNI (últimos 3)").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_dni = tk.Entry(frame, validate="key", validatecommand=(vcmd_dni, "%P"))
    entry_dni.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Teléfono").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_telefono = tk.Entry(frame, validate="key", validatecommand=(vcmd_tel, "%P"))
    entry_telefono.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame, text="El número telefónico debe contener entre 7 y 12 dígitos.",
             font=("Arial", 8), fg="gray").grid(row=3, column=1, sticky="w", padx=10)

    def limpiar_formulario():
        entry_nombre.delete(0, tk.END)
        entry_dni.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)

    def agregar_cliente():
        nombre = entry_nombre.get().strip()
        dni = entry_dni.get().strip()
        telefono = entry_telefono.get().strip()

        if len(telefono) < 7:
            messagebox.showerror("Error", "El número de teléfono debe tener al menos 7 dígitos.")
            return

        try:
            registrar_cliente(nombre, dni, telefono)
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            limpiar_formulario()
            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def guardar_cambios():
        cliente_id = estado["cliente_en_edicion"]
        if cliente_id is None:
            return

        nombre = entry_nombre.get().strip()
        telefono = entry_telefono.get().strip()

        if len(telefono) < 7:
            messagebox.showerror("Error", "El número de teléfono debe tener al menos 7 dígitos.")
            return

        try:
            actualizar_cliente(cliente_id, nombre, telefono)
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            limpiar_formulario()
            actualizar_tabla()
            btn_agregar.config(text="Agregar Cliente", command=agregar_cliente)
            estado["cliente_en_edicion"] = None
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_agregar = tk.Button(frame, text="Agregar Cliente", command=agregar_cliente)
    btn_agregar.grid(row=4, column=1, pady=10)

    columnas = ("ID", "Nombre", "DNI", "Teléfono", "Sesión", "Estado")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=100)
    tabla.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def actualizar_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for cliente in listar_clientes():
            cliente:Any
            tabla.insert("", "end", values=(
                cliente["id"],
                cliente["nombre"],
                cliente["dni_ultimos3"],
                cliente["telefono"],
                cliente["sesion_actual"],
                cliente["estado_pago"]
            ))

    def eliminar_cliente_seleccionado():
        seleccion = tabla.selection()
        if seleccion:
            cliente_id = tabla.item(seleccion[0])["values"][0]
            confirmacion = messagebox.askyesno("Confirmar", "¿Eliminar cliente seleccionado?")
            if confirmacion:
                borrar_cliente(cliente_id)
                actualizar_tabla()

    def editar_cliente_seleccionado():
        seleccion = tabla.selection()
        estado={}
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccioná un cliente para editar.")
            return

        valores = tabla.item(seleccion[0])["values"]
        entry_nombre.delete(0, tk.END)
        entry_dni.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)

        entry_nombre.insert(0, valores[1])
        entry_dni.insert(0, valores[2])
        entry_telefono.insert(0, valores[3])

        estado["cliente_en_edicion"] = valores[0]
        btn_agregar.config(text="Guardar Cambios", command=guardar_cambios)

    tk.Button(frame, text="Eliminar Cliente", command=eliminar_cliente_seleccionado).grid(row=7, column=1, pady=5)
    tk.Button(frame, text="Editar Cliente", command=editar_cliente_seleccionado).grid(row=8, column=1, pady=5)

    actualizar_tabla()

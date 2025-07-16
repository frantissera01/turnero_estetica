import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
from controllers.empleados_controller import (
    eliminar_empleado,
    registrar_empleado,
    listar_empleados,
    listar_empleados_inactivos,
    reactivar_empleado)
from views.historial_empleado_view import abrir_historial_empleado 

def abrir_empleados(contenedor):
    frame = tk.Frame(contenedor)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Registro de empleados ---
    tk.Label(frame, text="Nombre del empleado:").grid(row=0, column=0, sticky="e")
    entry_nombre = tk.Entry(frame)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame, text="Tarifa por hora ($):").grid(row=1, column=0, sticky="e")
    entry_tarifa = tk.Entry(frame)
    entry_tarifa.grid(row=1, column=1)

    # Validar que solo se puedan ingresar números en tarifa
    def solo_decimal(texto):
        try:
            if texto == "":
                return True
            float(texto)
            return True
        except ValueError:
            return False


    vcmd = frame.register(solo_decimal)
    entry_tarifa = tk.Entry(frame, validate="key", validatecommand=(vcmd, "%P"))
    entry_tarifa.grid(row=1, column=1)

    def agregar_empleado():
        nombre = entry_nombre.get().strip()
        tarifa_texto = entry_tarifa.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        if not tarifa_texto:
            messagebox.showerror("Error", "La tarifa no puede estar vacía.")
            return
        try:
            tarifa = float(tarifa_texto)
        except ValueError:
            messagebox.showerror("Error", "La tarifa debe ser un número válido.")
            return

        try:
            registrar_empleado(nombre, tarifa)
            messagebox.showinfo("Éxito", f"Empleado {nombre} registrado.")
            actualizar_tabla()
            entry_nombre.delete(0, tk.END)
            entry_tarifa.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Registrar empleado", command=agregar_empleado).grid(row=2, column=1, pady=5)

    # --- Tabla de empleados ---
    columnas = ("ID", "Nombre", "Tarifa")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=100)
    tabla.grid(row=4, column=0, columnspan=3, pady=10)

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        empleados: Any = listar_empleados()
        for emp in empleados:
            tabla.insert("", "end", values=(emp["id"], emp["nombre"], float(emp["tarifa_por_hora"])))

    actualizar_tabla()

    def ver_perfil():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccioná un empleado.")
            return

        valores = tabla.item(seleccionado)["values"]
        if valores:
            empleado_id = valores[0]
            abrir_historial_empleado(frame, empleado_id)

    tk.Button(frame, text="Ver perfil del empleado", command=ver_perfil).grid(row=5, column=1, pady=5)

    def eliminar_seleccionado():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccioná un empleado.")
            return

        valores = tabla.item(seleccionado)["values"]
        if valores:
            emp_id = valores[0]
            nombre = valores[1]
            confirmar = messagebox.askyesno("Eliminar", f"¿Deseás dar de baja al empleado {nombre}?")
            if confirmar:
                eliminar_empleado(emp_id)
                messagebox.showinfo("Empleado dado de baja", f"{nombre} fue eliminado del listado.")
                actualizar_tabla()

    tk.Button(frame, text="Eliminar empleado", command=eliminar_seleccionado, bg="red", fg="white").grid(row=6, column=1, pady=5)

    def ver_empleados_inactivos():
        ventana = tk.Toplevel(frame)
        ventana.title("Empleados dados de baja")
        ventana.geometry("400x300")
        ventana.grab_set()

        tabla_inactivos = ttk.Treeview(ventana, columns=("ID", "Nombre", "Tarifa"), show="headings")
        for col in ("ID", "Nombre", "Tarifa"):
            tabla_inactivos.heading(col, text=col)
            tabla_inactivos.column(col, anchor="center", width=120)
        tabla_inactivos.pack(fill="both", expand=True, padx=10, pady=10)

        empleados_inactivos = listar_empleados_inactivos()
        for emp in empleados_inactivos:
            emp:Any
            tabla_inactivos.insert("", "end", values=(emp["id"], emp["nombre"], emp["tarifa_por_hora"]))

        tk.Button(frame, text="Ver empleados inactivos", command=ver_empleados_inactivos).grid(row=7, column=1, pady=5)


        def reactivar_seleccionado():
            seleccionado = tabla_inactivos.focus()
            if not seleccionado:
                messagebox.showwarning("Atención", "Seleccioná un empleado.")
                return
            valores = tabla_inactivos.item(seleccionado)["values"]
            if valores:
                emp_id = valores[0]
                nombre = valores[1]
                confirmar = messagebox.askyesno("Reactivar", f"¿Deseás reactivar al empleado {nombre}?")
                if confirmar:
                    reactivar_empleado(emp_id)
                    messagebox.showinfo("Reactivado", f"{nombre} fue reactivado correctamente.")
                    ventana.destroy()
                    actualizar_tabla()

        tk.Button(ventana, text="Reactivar empleado", command=reactivar_seleccionado, bg="green", fg="white").pack(pady=5)



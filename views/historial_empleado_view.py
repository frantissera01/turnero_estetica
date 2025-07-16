import tkinter as tk
from tkinter import ttk, messagebox
from controllers.historial_controller import obtener_perfil_empleado, abonar_empleado

def abrir_historial_empleado(root, empleado_id):
    datos = obtener_perfil_empleado(empleado_id)

    ventana = tk.Toplevel(root)
    ventana.title(f"Perfil de {datos['nombre']}")
    ventana.geometry("650x500")
    ventana.grab_set()

    # --- Resumen de pagos ---
    tk.Label(ventana, text=f"Empleado: {datos['nombre']}", font=("Arial", 14, "bold")).pack(pady=5)
    tk.Label(ventana, text=f"Tarifa por hora: ${int(datos['tarifa']):,}".replace(",", ".")).pack()
    tk.Label(ventana, text=f"Monto a cobrar: ${int(datos['total_a_cobrar']):,}".replace(",", "."), fg="blue").pack()


    # Mostrar último pago (fecha y monto si existe)
    ultimo_pago = datos.get("ultimo_pago", {})
    if ultimo_pago and "fecha" in ultimo_pago and "monto" in ultimo_pago:
        tk.Label(
            ventana,
            text=f"Último pago: {datos['ultimo_pago']['fecha']} - ${int(datos['ultimo_pago']['monto']):,}".replace(",", "."),
            fg="green"
        ).pack()
    else:
        tk.Label(ventana, text="Último pago: sin registro", fg="gray").pack()

    tk.Label(ventana, text=f"Total pagado acumulado: ${int(datos['total_pagado']):,}".replace(",", ".")).pack(pady=5)

    # --- Tabla de historial ---
    columnas = ("Fecha", "Horas", "Monto Diario")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=200)
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    for registro in reversed(datos["historial"]):
        monto_dia = registro.get("monto_dia", 0.0) or 0.0
        tabla.insert("", "end", values=(
            registro["fecha"],
            f"{registro['horas_trabajadas']:.2f}",
            f"${int(monto_dia):,}".replace(",", ".")
        ))

    # --- Función de abono manual ---
    def abonar():
        ventana_abono = tk.Toplevel(ventana)
        ventana_abono.title("Registrar abono manual")
        ventana_abono.geometry("300x150")
        ventana_abono.grab_set()

        entry_monto = tk.Entry(ventana_abono, justify="right")
        entry_monto.pack(pady=5)

        def formatear_en_tiempo_real(*args):
            valor = monto_var.get().replace(".", "")
            if valor.isdigit():
                numero = int(valor)
                formateado = f"{numero:,}".replace(",", ".")
                monto_var.set(formateado)
            elif valor != "":
                monto_var.set("")

        monto_var = tk.StringVar()
        monto_var.trace_add("write", formatear_en_tiempo_real)
        entry_monto.config(textvariable=monto_var)

        def confirmar_abono():
            monto_str = monto_var.get().replace(".", "")
            try:
                monto = float(monto_str)
                if monto <= 0:
                    raise ValueError("Debe ser mayor a cero")
            except ValueError:
                messagebox.showerror("Error", "Ingresá un monto válido.")
                return

            abonar_empleado(empleado_id, monto)
            messagebox.showinfo("Éxito", f"Se abonaron ${int(monto):,}".replace(",", "."))
            ventana_abono.destroy()
            ventana.destroy()
            abrir_historial_empleado(root, empleado_id)  # Recarga la vista

        tk.Button(ventana_abono, text="Confirmar", command=confirmar_abono, bg="green", fg="white").pack(pady=10)

    tk.Button(ventana, text="Abonar", command=abonar, bg="blue", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

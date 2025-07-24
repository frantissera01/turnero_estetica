import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from controllers.clientes_controller import listar_clientes_por_dni, registrar_cliente
from controllers.turnos_controller import listar_turnos, registrar_turno, borrar_turno_controller
from models.db import conectar
from typing import Any

def mostrar_turno(frame_contenido, fecha, hora, botones_turnos, mostrar_semana):
    def actualizar_boton(fecha, hora):
        btn = botones_turnos.get((fecha, hora))
        if btn:
            fecha_str = fecha.strftime("%Y-%m-%d")
            hora_str = f"{hora:02d}:00:00"
            cantidad = len(listar_turnos(fecha_str, hora_str))
            color = "lightgreen" if cantidad < 5 else "tomato"
            btn.config(text=f"{cantidad} / 5", bg=color)
    
    for widget in frame_contenido.winfo_children(): 
        widget.destroy()

    btn_volver = tk.Button(frame_contenido, text="⬅ Volver", command=lambda: mostrar_semana(frame_contenido, fecha, botones_turnos))
    btn_volver.pack(anchor="w", padx=10, pady=10)

    lbl = tk.Label(frame_contenido, text=f"Turno {hora}:00 - {fecha.strftime('%d/%m/%Y')}", font=("Arial", 14))
    lbl.pack(pady=10)

    lista_box = tk.Listbox(frame_contenido, width=50, height=10)
    lista_box.pack(pady=5)

    fecha_str = fecha.strftime("%Y-%m-%d")
    hora_str = f"{hora:02d}:00:00"

    def cargar_lista_turnos():
        lista_box.delete(0, tk.END)
        turnos = listar_turnos(fecha_str, hora_str)
        turnos:Any
        for t in turnos:
            lista_box.insert(tk.END, f"{t['nombre_cliente']} (DNI: {t['dni_ultimos3']}) - TurnoID: {t['turno_id']}")

    cargar_lista_turnos()

    def buscar_por_dni():
        popup = tk.Toplevel(frame_contenido)
        popup.title("Buscar clienta")
        popup.geometry("300x150")

        tk.Label(popup, text="Ingrese últimos 3 dígitos del DNI:").pack(pady=5)
        entry_dni = tk.Entry(popup)
        entry_dni.pack(pady=5)

        def confirmar():
            dni = entry_dni.get().strip()
            popup.destroy()
            clientas = listar_clientes_por_dni(dni)

            if not clientas:
                if messagebox.askyesno("No encontrada", "No hay clientas con ese DNI. ¿Registrar nueva?"):
                    registrar_nueva(dni)
                return

            if len(clientas) == 1:
                agendar(clientas[0])
            else:
                elegir_clienta(clientas)

        tk.Button(popup, text="Buscar", command=confirmar).pack(pady=5)

    def registrar_nueva(dni):
        popup = tk.Toplevel(frame_contenido)
        popup.title("Registrar clienta")
        popup.geometry("300x200")

        tk.Label(popup, text="Nombre:").pack()
        entry_nombre = tk.Entry(popup)
        entry_nombre.pack()

        tk.Label(popup, text="Teléfono:").pack()
        entry_telefono = tk.Entry(popup)
        entry_telefono.pack()

        def confirmar_registro():
            nombre = entry_nombre.get().strip()
            telefono = entry_telefono.get().strip()
            try:
                registrar_cliente(nombre, dni, telefono)
                nueva = listar_clientes_por_dni(dni)[-1]
                agendar(nueva)
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Registrar", command=confirmar_registro).pack(pady=10)

    def elegir_clienta(lista_clientas):
        popup = tk.Toplevel(frame_contenido)
        popup.title("Seleccionar clienta")
        popup.geometry("300x200")
        tk.Label(popup, text="Seleccioná una clienta:").pack()

        seleccion = tk.StringVar()
        for c in lista_clientas:
            texto = f"{c['nombre']} - Tel: {c['telefono']} - ID: {c['id']}"
            tk.Radiobutton(popup, text=texto, variable=seleccion, value=c["id"]).pack(anchor="w")

        def confirmar():
            id_seleccionado = seleccion.get()
            if id_seleccionado:
                clienta = next(c for c in lista_clientas if str(c["id"]) == id_seleccionado)
                agendar(clienta)
                popup.destroy()

        tk.Button(popup, text="Agendar", command=confirmar).pack(pady=10)

    def agendar(clienta):
        if len(listar_turnos(fecha_str, hora_str)) >= 5:
            messagebox.showwarning("Límite alcanzado", "Ya hay 5 clientas en este turno.")
            return

        try:
            registrar_turno(clienta["id"], fecha_str, hora_str)
            cargar_lista_turnos()
            actualizar_boton(fecha, hora)
            messagebox.showinfo("Éxito", f"{clienta['nombre']} fue agendada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar():
        seleccion = lista_box.curselection()
        if seleccion:
            texto = lista_box.get(seleccion)
            if "TurnoID:" in texto:
                try:
                    turno_id = int(texto.split("TurnoID:")[1].strip())
                    borrar_turno_controller(turno_id)
                    cargar_lista_turnos()
                    actualizar_boton(fecha, hora)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def mover_turno():
        seleccion = lista_box.curselection()
        if not seleccion:
            messagebox.showwarning("Seleccioná un turno", "Seleccioná una clienta para mover.")
            return

        index = seleccion[0]
        texto = lista_box.get(index)

        if "TurnoID:" not in texto:
            messagebox.showerror("Error", "No se encontró el ID del turno.")
            return

        turno_id = int(texto.split("TurnoID:")[1].strip())

        popup = tk.Toplevel(frame_contenido)
        popup.title("Mover Turno")
        popup.geometry("300x200")

        tk.Label(popup, text="Nueva fecha (AAAA-MM-DD):").pack(pady=5)
        entry_fecha = tk.Entry(popup)
        entry_fecha.insert(0, fecha_str)
        entry_fecha.pack()

        tk.Label(popup, text="Nueva hora (07 a 20):").pack(pady=5)
        hora_var = tk.StringVar(popup)
        hora_var.set(f"{hora:02d}:00:00")
        opciones_hora = [f"{h:02d}:00:00" for h in range(7, 21)]
        dropdown = tk.OptionMenu(popup, hora_var, *opciones_hora)
        dropdown.pack()

        def confirmar():
            nueva_fecha = entry_fecha.get().strip()
            nueva_hora = hora_var.get().strip()

            try:
                if len(listar_turnos(nueva_fecha, nueva_hora)) >= 5:
                    messagebox.showwarning("Sin lugar", "Ese turno ya tiene 5 clientas.")
                    return

                conn = conectar()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE turnos SET fecha=%s, hora=%s WHERE id=%s",
                    (nueva_fecha, nueva_hora, turno_id)
                )
                conn.commit()
                conn.close()

                popup.destroy()
                cargar_lista_turnos()
                actualizar_boton(fecha, hora)
                nueva_fecha_obj = datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
                nueva_hora_int = int(nueva_hora[:2])
                actualizar_boton(nueva_fecha_obj, nueva_hora_int)

                messagebox.showinfo("Éxito", "Turno movido correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo mover el turno: {e}")

        tk.Button(popup, text="Mover", command=confirmar).pack(pady=10)

    tk.Button(frame_contenido, text="Buscar/Agregar clienta", command=buscar_por_dni).pack(pady=5)
    tk.Button(frame_contenido, text="Eliminar seleccionada", command=eliminar).pack(pady=5)
    tk.Button(frame_contenido, text="Mover seleccionada", command=mover_turno).pack(pady=5)

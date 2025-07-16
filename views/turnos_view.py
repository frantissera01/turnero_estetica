import tkinter as tk
import calendar
from models.db import conectar
from tkinter import Frame, Widget 
from datetime import datetime, timedelta, date
from tkinter import messagebox
from controllers.clientes_controller import listar_clientes_por_dni, registrar_cliente
from controllers.turnos_controller import listar_turnos, registrar_turno, borrar_turno_controller
from typing import Any

def abrir_turnero(frame_contenido: Frame):
    # Limpia el contenido previo
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    año_actual = datetime.now().year
    estado = {"anio": año_actual}
    botones_turnos = {}
    

    # FRAME SUPERIOR: navegación por año
    frame_superior = tk.Frame(frame_contenido)
    frame_superior.pack(pady=10)

    btn_prev = tk.Button(frame_superior, text="◀", command=lambda: cambiar_anio(-1))
    btn_prev.pack(side=tk.LEFT, padx=10)

    lbl_anio = tk.Label(frame_superior, text=str(estado["anio"]), font=("Arial", 12, "bold"))
    lbl_anio.pack(side=tk.LEFT)

    btn_next = tk.Button(frame_superior, text="▶", command=lambda: cambiar_anio(1))
    btn_next.pack(side=tk.LEFT, padx=10)

    frame_meses = tk.Frame(frame_contenido)
    frame_meses.pack(pady=20)

    def cambiar_anio(delta):
        estado["anio"] += delta
        lbl_anio.config(text=str(estado["anio"]))
        mostrar_meses()

    def mostrar_meses():
        for widget in frame_meses.winfo_children():
            widget.destroy()

        meses = list(calendar.month_name)[1:]
        for i, mes in enumerate(meses):
            btn = tk.Button(frame_meses, text=mes, width=15, height=2,
                            command=lambda m=i+1: mostrar_calendario_mes(m, estado["anio"]))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)

    def mostrar_calendario_mes(mes, anio):
        for widget in frame_contenido.winfo_children():
            widget.destroy()

        btn_volver = tk.Button(frame_contenido, text="⬅ Volver", command=lambda: abrir_turnero(frame_contenido))
        btn_volver.pack(anchor="w", padx=10, pady=10)

        lbl_mes = tk.Label(frame_contenido, text=f"{calendar.month_name[mes]} {anio}", font=("Arial", 14, "bold"))
        lbl_mes.pack()

        frame_cal = tk.Frame(frame_contenido)
        frame_cal.pack(pady=20)

        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for i, dia in enumerate(dias):
            tk.Label(frame_cal, text=dia, font=("Arial", 10, "bold"), padx=10).grid(row=0, column=i)

        cal = calendar.monthcalendar(anio, mes)
        for fila, semana in enumerate(cal, start=1):
            for col, dia in enumerate(semana):
                if dia != 0:
                    btn = tk.Button(frame_cal, text=str(dia), width=4,
                                    command=lambda d=dia: mostrar_semana(date(anio, mes, d)))
                    btn.grid(row=fila, column=col, padx=2, pady=2)

    def mostrar_semana(fecha):
        for widget in frame_contenido.winfo_children():
            widget.destroy()

        btn_volver = tk.Button(frame_contenido, text="⬅ Volver", command=lambda: mostrar_calendario_mes(fecha.month, fecha.year))
        btn_volver.pack(anchor="w", padx=10, pady=10)

        lbl_titulo = tk.Label(frame_contenido, text=f"Semana de {fecha.strftime('%d/%m/%Y')}", font=("Arial", 14, "bold"))
        lbl_titulo.pack()

        frame = tk.Frame(frame_contenido)
        frame.pack(padx=10, pady=10)

        dia_semana = fecha.weekday()
        inicio_semana = fecha - timedelta(days=dia_semana)
        dias_semana = [inicio_semana + timedelta(days=i) for i in range(6)]
        horas = list(range(7, 21))

        tk.Label(frame, text="Hora", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        for i, d in enumerate(dias_semana):
            nombre_dia = d.strftime("%a %d/%m")
            tk.Label(frame, text=nombre_dia, font=("Arial", 10, "bold")).grid(row=0, column=i+1, padx=5, pady=5)

        botones_turnos.clear()
        for f, h in enumerate(horas):
            tk.Label(frame, text=f"{h}:00", font=("Arial", 10)).grid(row=f+1, column=0, padx=5, pady=5)
            for c, fecha_dia in enumerate(dias_semana):
                fecha_str = fecha_dia.strftime("%Y-%m-%d")
                hora_str = f"{h:02d}:00:00"
                turnos = listar_turnos(fecha_str, hora_str)
                cantidad = len(turnos)
                color = "lightgreen" if cantidad < 5 else "tomato"

                btn = tk.Button(frame, text=f"{cantidad} / 5", bg=color, width=10,
                                command=lambda f=fecha_dia, h=h: mostrar_turno(frame_contenido, f, h))
                btn.grid(row=f+1, column=c+1, padx=2, pady=2)
                botones_turnos[(fecha_dia, h)] = btn

        
    def mostrar_turno(frame, fecha, hora):
        def actualizar_boton(fecha, hora):
            btn = botones_turnos.get((fecha, hora))
            if btn:
                fecha_str = fecha.strftime("%Y-%m-%d")
                hora_str = f"{hora:02d}:00:00"
                cantidad = len(listar_turnos(fecha_str, hora_str))
                color = "lightgreen" if cantidad < 5 else "tomato"
                btn.config(text=f"{cantidad} / 5", bg=color)
        
        for widget in frame.winfo_children(): 
            widget: tk.Widget
            widget.destroy()

        btn_volver = tk.Button(frame, text="⬅ Volver", command=lambda: mostrar_semana(fecha))
        btn_volver.pack(anchor="w", padx=10, pady=10)

        lbl = tk.Label(frame, text=f"Turno {hora}:00 - {fecha.strftime('%d/%m/%Y')}", font=("Arial", 14))
        lbl.pack(pady=10)

        lista_box = tk.Listbox(frame, width=50, height=10)
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
            popup = tk.Toplevel(frame)
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
            popup = tk.Toplevel(frame)
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
            popup = tk.Toplevel(frame)
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
                print("DEBUG clienta encontrada:", clienta)
                registrar_turno(clienta["id"], fecha_str, hora_str)
                # Obtener el turno recién creado
                nuevos_turnos = listar_turnos(fecha_str, hora_str)
                nuevos_turnos:Any
                turno_cliente = next((t for t in nuevos_turnos if t["cliente_id"] == clienta["id"]), None)
                if turno_cliente:
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


            popup = tk.Toplevel(frame)
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
                    # También actualiza el nuevo botón del día/hora destino
                    nueva_fecha_obj = datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
                    nueva_hora_int = int(nueva_hora[:2])
                    actualizar_boton(nueva_fecha_obj, nueva_hora_int)

                    messagebox.showinfo("Éxito", "Turno movido correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo mover el turno: {e}")

            tk.Button(popup, text="Mover", command=confirmar).pack(pady=10)
        tk.Button(frame, text="Buscar/Agregar clienta", command=buscar_por_dni).pack(pady=5)
        tk.Button(frame, text="Eliminar seleccionada", command=eliminar).pack(pady=5)
        tk.Button(frame, text="Mover seleccionada", command=mover_turno).pack(pady=5)


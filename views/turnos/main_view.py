import tkinter as tk
import calendar
from datetime import datetime, timedelta, date

from .turno_detalle import mostrar_turno
from controllers.clientes_controller import listar_clientes_por_dni, registrar_cliente
from controllers.turnos_controller import listar_turnos, registrar_turno, borrar_turno_controller


def abrir_turnero(frame_contenido: tk.Frame):
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    año_actual = datetime.now().year
    estado = {"anio": año_actual}
    botones_turnos = {}

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
                                command=lambda f=fecha_dia, h=h: mostrar_turno(frame_contenido, f, h, botones_turnos, mostrar_semana))
                btn.grid(row=f+1, column=c+1, padx=2, pady=2)
                botones_turnos[(fecha_dia, h)] = btn

    mostrar_meses()

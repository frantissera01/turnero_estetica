from models.turnos_model import TurnosModel
from models.clientes_model import ClientesModel
from datetime import date, timedelta

class TurnosController:
    HORAS = [f"{h:02d}:00:00" for h in range(7, 21)]  # 07..20

    def __init__(self, view):
        self.view = view
        self.model = TurnosModel()
        self.clientes_model = ClientesModel()
        self.ref = date.today()

    def _rango_semana(self):
        lunes = self.ref - timedelta(days=(self.ref.weekday()))
        sab = lunes + timedelta(days=5)
        return lunes, sab

    def cargar_semana(self):
        ini, fin = self._rango_semana()
        counts = {(str(r.get("fecha")), str(r.get("hora"))): int(r.get("cantidad", 0)) for r in rows}  # type: ignore
        self.view.render_grid(ini, fin, self.HORAS, counts, self.model.MAX_POR_HORA)

    def anterior(self):
        self.ref -= timedelta(days=7)
        self.cargar_semana()

    def siguiente(self):
        self.ref += timedelta(days=7)
        self.cargar_semana()

    def listar_slot(self, fecha, hora):
        turnos = self.model.listar_slot(fecha, hora)
        self.view.mostrar_slot(fecha, hora, turnos)

    def clientes_opciones(self):
        return self.clientes_model.obtener_clientes()

    def crear_turno(self, cliente_id, fecha, hora):
        actuales = self.model.listar_slot(fecha, hora)
        if len(actuales) >= self.model.MAX_POR_HORA:
            self.view.alerta("Límite alcanzado (5 por hora)")
            return
        self.model.crear(cliente_id, fecha, hora)
        self.cargar_semana()
        self.listar_slot(fecha, hora)

    def mover_turno(self, turno_id, nueva_fecha, nueva_hora):
        actuales = self.model.listar_slot(nueva_fecha, nueva_hora)
        if len(actuales) >= self.model.MAX_POR_HORA:
            self.view.alerta("No se puede mover: destino lleno (5)")
            return
        self.model.mover(turno_id, nueva_fecha, nueva_hora)
        self.cargar_semana()
        self.listar_slot(nueva_fecha, nueva_hora)

    def eliminar_turno(self, turno_id, fecha, hora):
        self.model.eliminar(turno_id)
        self.cargar_semana()
        self.listar_slot(fecha, hora)

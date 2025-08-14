class MainController:
    def __init__(self, root):
        self.root = root

    def abrir_gestion_empleados(self):
        from views.empleados_view import EmpleadosView
        self._abrir_en_frame(EmpleadosView)

    def abrir_gestion_clientes(self):
        from views.clientes_view import ClientesView
        self._abrir_en_frame(ClientesView)

    def abrir_turnos(self):
        from views.turnos_view import TurnosView
        self._abrir_en_frame(TurnosView)

    def _abrir_en_frame(self, ViewClass):
        for widget in self.root.winfo_children():
            widget.destroy()
        ViewClass(self.root)

    def abrir_horarios(self):
        from views.horarios_view import HorariosView
        self._abrir_en_frame(HorariosView)

    def abrir_planes(self):
        from views.planes_view import PlanesView
        self._abrir_en_frame(PlanesView)

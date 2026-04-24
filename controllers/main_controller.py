# controllers/main_controller.py
class MainController:
    def __init__(self, root, main_view):
        self.root = root
        self.view = main_view  # referencia al MainView

    def _abrir(self, ViewCls):
        # carga la vista dentro del contenedor y le pasa un on_back
        self.view.open_in_content(lambda parent: ViewCls(parent, on_back=self.view.render_home))

    def abrir_gestion_empleados(self):
        from views.empleados_view import EmpleadosView
        self._abrir(EmpleadosView)

    def abrir_gestion_clientes(self):
        from views.clientes_view import ClientesView
        self._abrir(ClientesView)

    def abrir_turnos(self):
        from views.turnos_view import TurnosView
        self._abrir(TurnosView)

    def abrir_horarios(self):
        from views.horarios_view import HorariosView
        self._abrir(HorariosView)

    def abrir_planes(self):
        from views.planes_view import PlanesView
        self._abrir(PlanesView)

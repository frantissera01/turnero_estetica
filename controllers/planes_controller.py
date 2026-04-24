from models.planes_model import PlanesModel

class PlanesController:
    def __init__(self, view):
        self.view = view
        self.model = PlanesModel()

    # ---- PLANES ----
    def cargar_planes(self):
        planes = self.model.listar_planes()
        self.view.mostrar_planes(planes)

    def crear_plan(self, nombre, descripcion, total_sesiones, precio):
        # Validaciones mínimas
        if not nombre or int(total_sesiones) <= 0:
            self.view.alerta("Nombre y total de sesiones son obligatorios y > 0.")
            return
        try:
            precio_val = float(precio)
        except:
            self.view.alerta("Precio inválido.")
            return

        self.model.crear_plan(nombre, descripcion, int(total_sesiones), precio_val)
        self.view.alerta("Plan creado.")
        self.cargar_planes()

    def actualizar_plan(self, plan_id, nombre, descripcion, total_sesiones, precio):
        if not plan_id:
            self.view.alerta("Seleccioná un plan.")
            return
        try:
            precio_val = float(precio)
        except:
            self.view.alerta("Precio inválido.")
            return

        self.model.actualizar_plan(plan_id, nombre, descripcion, int(total_sesiones), precio_val)
        self.view.alerta("Plan actualizado.")
        self.cargar_planes()

    def eliminar_plan(self, plan_id):
        if not plan_id:
            self.view.alerta("Seleccioná un plan.")
            return
        self.model.eliminar_plan(plan_id)
        self.view.alerta("Plan eliminado.")
        self.cargar_planes()

    # ---- ASIGNACIONES ----
    def cargar_combo_clientes(self):
        return self.model.listar_clientes()

    def cargar_combo_planes(self):
        return self.model.listar_planes()

    def cargar_asignaciones(self):
        asign = self.model.listar_asignaciones()

        def safe_int(x, default=0):
            try:
                # Convierte Decimal/date/datetime/None a str y luego a int si es posible
                return int(str(x))
            except (ValueError, TypeError):
                return default

        datos = []
        for a in asign:
            if isinstance(a, dict):
                total  = safe_int(a.get("total_sesiones", 0))
                usadas = safe_int(a.get("sesiones_usadas", 0))
                restantes = max(total - usadas, 0)
                datos.append({
                    "id": a.get("id"),
                    "cliente": f"{a.get('c_nombre','')} {a.get('c_apellido','')}",
                    "plan": a.get("p_nombre",""),
                    "fecha_inicio": a.get("fecha_inicio"),
                    "usadas": usadas,
                    "total": total,
                    "restantes": restantes
                })
            else:
                # tupla: (0)id, (1)cliente_id, (2)plan_id, (3)fecha_inicio,
                #        (4)sesiones_usadas, (5)c_nombre, (6)c_apellido,
                #        (7)p_nombre, (8)total_sesiones
                total  = safe_int(a[8])
                usadas = safe_int(a[4])
                restantes = max(total - usadas, 0)
                datos.append({
                    "id": a[0],
                    "cliente": f"{a[5]} {a[6]}",
                    "plan": a[7],
                    "fecha_inicio": a[3],
                    "usadas": usadas,
                    "total": total,
                    "restantes": restantes
                })

        self.view.mostrar_asignaciones(datos)


    def asignar_plan(self, cliente_id, plan_id, fecha_inicio):
        if not cliente_id or not plan_id or not fecha_inicio:
            self.view.alerta("Cliente, plan y fecha de inicio son obligatorios.")
            return
        self.model.asignar_plan(cliente_id, plan_id, fecha_inicio)
        self.view.alerta("Plan asignado.")
        self.cargar_asignaciones()

    def eliminar_asignacion(self, asignacion_id):
        if not asignacion_id:
            self.view.alerta("Seleccioná una asignación.")
            return
        self.model.eliminar_asignacion(asignacion_id)
        self.view.alerta("Asignación eliminada.")
        self.cargar_asignaciones()

    def marcar_uso(self, asignacion_id):
        ok, msg = self.model.marcar_sesion_usada(asignacion_id)
        self.view.alerta(msg)
        if ok:
            self.cargar_asignaciones()

    def revertir_uso(self, asignacion_id):
        ok, msg = self.model.marcar_sesion_revertir(asignacion_id)
        self.view.alerta(msg)
        if ok:
            self.cargar_asignaciones()

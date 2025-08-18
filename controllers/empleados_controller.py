from models.empleados_model import EmpleadosModel

def _safe_str(x):
    return "" if x is None else str(x)

def _safe_float(x, default=0.0):
    try:
        return float(x) if x is not None else default
    except Exception:
        try:
            return float(str(x))
        except Exception:
            return default
        
class EmpleadosController:
    def __init__(self, view):
        self.view = view
        self.model = EmpleadosModel()

    def cargar(self):
        rows = self.model.listar()
        datos = []
        for r in rows:
            if isinstance(r, dict):
                datos.append({
                    "id": r.get("id"),
                    "nombre": _safe_str(r.get("nombre")),
                    "apellido": _safe_str(r.get("apellido")),
                    "tarifa_hora": _safe_float(r.get("tarifa_hora")),
                })
            else:
                # tupla: id, nombre, apellido, telefono, documento, tarifa_hora
                datos.append({
                    "id": r[0],
                    "nombre": _safe_str(r[1]),
                    "apellido": _safe_str(r[2]),
                    "tarifa_hora": _safe_float(r[5]),
                })
        self.view.mostrar_empleados(datos)

    def guardar(self, datos):
        if datos["id"] is None:
            self.model.insertar(datos)
        else:
            self.model.actualizar(datos)
        self.cargar()

    def eliminar(self, empleado_id):
        self.model.eliminar_empleado(empleado_id)
        self.cargar()

    def lista_empleados(self):
        return self.model.listar()

    def cargar_saldos(self):
        rows = self.model.listar_saldos_pendientes()
        data = []
        for r in rows:
            if isinstance(r, dict):
                rid   = r.get("id")
                nom   = f"{r.get('nombre','')} {r.get('apellido','')}"
                deve  = _safe_float(r.get("devengado", 0))
                pag   = _safe_float(r.get("pagado", 0))
                saldo = _safe_float(r.get("saldo", 0))
            else:
                rid   = r[0]
                nom   = f"{r[1]} {r[2]}"
                deve  = _safe_float(r[3])
                pag   = _safe_float(r[4])
                saldo = _safe_float(r[5])
            data.append({
                "empleado_id": int(str(rid)),
                "empleado": nom,
                "devengado": deve,
                "pagado": pag,
                "saldo": saldo
            })
        self.view.mostrar_saldos(data)

    def pagar_total(self, empleado_id: int):
        # carga saldos y busca el del empleado
        rows = self.model.listar_saldos_pendientes()
        saldo_emp = 0.0
        for r in rows:
            rid = r.get("id") if isinstance(r, dict) else r[0]
            if int(str(rid)) == empleado_id:
                saldo_emp = _safe_float(r.get("saldo", 0) if isinstance(r, dict) else r[5])
                break
        if saldo_emp <= 0:
            self.view.alerta("No hay saldo pendiente para este empleado.")
            return
        self.model.registrar_pago(empleado_id, saldo_emp, observacion="Pago total")
        self.view.alerta("Pago total registrado.")
        self.cargar_saldos()

    def pagar_parcial(self, empleado_id: int, monto: float):
        if monto <= 0:
            self.view.alerta("El monto debe ser mayor a 0.")
            return

        # Validar contra saldo actual
        rows = self.model.listar_saldos_pendientes()
        saldo_emp = 0.0
        for r in rows:
            rid = r.get("id") if isinstance(r, dict) else r[0]
            if int(str(rid)) == empleado_id:
                saldo_emp = _safe_float(r.get("saldo", 0) if isinstance(r, dict) else r[5])
                break

        if saldo_emp <= 0:
            self.view.alerta("No hay saldo pendiente para este empleado.")
            return
        if monto > saldo_emp:
            self.view.alerta(f"El monto supera el saldo (${saldo_emp:.2f}).")
            return

        self.model.registrar_pago(empleado_id, monto, observacion="Pago parcial")
        self.view.alerta(f"Pago de ${monto:.2f} registrado.")
        self.cargar_saldos()
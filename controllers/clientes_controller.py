from models.clientes_model import ClientesModel

class ClientesController:
    def __init__(self, view):
        self.view = view
        self.model = ClientesModel()

    def cargar(self):
        clientes = self.model.obtener_clientes()
        self.view.mostrar_clientes(clientes)

    def guardar(self, datos):
        cid = datos.get("id")
        args = (
            datos["nombre"], datos["apellido"], datos["telefono"], datos["documento"],
            int(datos.get("sesiones", 0) or 0), datos.get("estado_pago", "PENDIENTE")
        )
        if cid:
            self.model.actualizar_cliente(cid, *args)
        else:
            self.model.agregar_cliente(*args)
        self.cargar()

    def eliminar(self, cliente_id):
        self.model.eliminar_cliente(cliente_id)
        self.cargar()
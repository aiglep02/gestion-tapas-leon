from modelos.logica.EmpleadoService import EmpleadoService

class ControladorEmpleado:
    def __init__(self):
        self.service = EmpleadoService()

    def obtener_pedidos_pendientes(self):
        return self.service.obtener_pedidos_pendientes()

    def actualizar_estado_pedido(self, id_pedido, nuevo_estado):
        return self.service.actualizar_estado_pedido(id_pedido, nuevo_estado)

    def entregar_pedido(self, id_pedido, nombre_tapa, cantidad):
        return self.service.entregar_pedido(id_pedido, nombre_tapa, cantidad)

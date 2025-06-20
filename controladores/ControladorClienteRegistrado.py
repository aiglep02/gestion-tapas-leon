from modelos.logica.ClienteService import ClienteService

class ControladorClienteRegistrado:
    def __init__(self, conexion):
        self.service = ClienteService(conexion)

    def obtener_tapas_disponibles(self):
        """Devuelve la lista de tapas (id, nombre, stock)."""
        return self.service.obtener_tapas_disponibles()

    def hacer_pedido(self, usuario_id, id_tapa, cantidad):
        """Realiza un pedido a través del servicio. Devuelve mensaje de error o None si todo va bien."""
        return self.service.hacer_pedido(usuario_id, id_tapa, cantidad)

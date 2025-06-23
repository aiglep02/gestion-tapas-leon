# controladores/ControladorPedido.py

from modelos.logica.PedidoService import PedidoService

class ControladorPedido:
    def __init__(self, conexion):
        self.service = PedidoService(conexion)

    def crear_pedido(self, id_usuario, id_tapa, cantidad):
        return self.service.crear_pedido(id_usuario, id_tapa, cantidad)

    def obtener_pedidos_usuario(self, id_usuario):
        return self.service.obtener_pedidos_usuario(id_usuario)

    def cambiar_estado_pedido(self, id_pedido, nuevo_estado):
        return self.service.cambiar_estado_pedido(id_pedido, nuevo_estado)

    def eliminar_pedido(self, id_pedido):
        return self.service.eliminar_pedido(id_pedido)

    def cambiar_tapa_pedido(self, id_pedido, nueva_tapa_id):
        return self.service.cambiar_tapa_pedido(id_pedido, nueva_tapa_id)

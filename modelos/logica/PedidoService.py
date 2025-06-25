from modelos.vo.pedidoVO import PedidoVO
from modelos.dao.pedidoDAO import PedidoDAO

class PedidoService:
    def __init__(self):
        self.pedido_dao = PedidoDAO() 
        
    def crear_pedido(self, id_usuario, id_tapa, cantidad):
        pedido = PedidoVO(id_usuario=id_usuario, id_tapa=id_tapa, cantidad=cantidad)
        pedido_id = self.pedido_dao.insertar_pedido(pedido)
        return pedido_id is not None

    def obtener_pedidos_usuario(self, id_usuario):
        return self.pedido_dao.obtener_pedidos_por_usuario(id_usuario)

    def cambiar_estado_pedido(self, id_pedido, nuevo_estado):
        return self.pedido_dao.actualizar_estado_pedido(id_pedido, nuevo_estado)

    def eliminar_pedido(self, id_pedido):
        return self.pedido_dao.eliminar_pedido(id_pedido)

    def cambiar_tapa_pedido(self, id_pedido, nueva_tapa_id):
        return self.pedido_dao.actualizar_tapa_pedido(id_pedido, nueva_tapa_id)

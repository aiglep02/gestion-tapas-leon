from modelos.dao.pedidoDAO import PedidoDAO
from modelos.dao.tapaDAO import TapaDAO

class EmpleadoService:
    def __init__(self, conexion):
        self.pedido_dao = PedidoDAO(conexion)
        self.tapa_dao = TapaDAO(conexion)

    def obtener_pedidos_pendientes(self):
        return self.pedido_dao.obtener_pedidos_pendientes()

    def actualizar_estado_pedido(self, id_pedido, nuevo_estado):
        return self.pedido_dao.actualizar_estado_pedido(id_pedido, nuevo_estado)

    def entregar_pedido(self, id_pedido, id_tapa, cantidad):
        exito_estado = self.pedido_dao.actualizar_estado_pedido(id_pedido, "entregado")
        if exito_estado:
            return self.tapa_dao.reducir_stock_por_id(id_tapa, cantidad)
        return False

    def obtener_nombre_tapa(self, id_tapa):
        return self.tapa_dao.obtener_nombre_por_id(id_tapa)

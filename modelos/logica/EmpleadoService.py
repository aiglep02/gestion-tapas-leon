from modelos.dao.pedidoDAO import PedidoDAO
from modelos.dao.tapaDAO import TapaDAO

class EmpleadoService:
    def __init__(self):
        self.pedido_dao = PedidoDAO()
        self.tapa_dao = TapaDAO()

    def obtener_pedidos_pendientes(self):
        return self.pedido_dao.obtener_pedidos_pendientes()

    def actualizar_estado_pedido(self, id_pedido, nuevo_estado):
        return self.pedido_dao.actualizar_estado_pedido(id_pedido, nuevo_estado)

    def entregar_pedido(self, id_pedido, nombre_tapa, cantidad):
        exito_estado = self.pedido_dao.actualizar_estado_pedido(id_pedido, "entregado")
        if exito_estado:
            self.tapa_dao.reducir_stock_por_nombre(nombre_tapa, cantidad)
            return True
        return False

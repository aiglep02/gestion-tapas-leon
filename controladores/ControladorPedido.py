from modelos.PedidoDAO import PedidoDAO
from modelos.LineaPedidoDAO import LineaPedidoDAO
from modelos.PedidoVO import PedidoVO
from modelos.LineaPedidoVO import LineaPedidoVO

class ControladorPedido:
    def __init__(self, conexion):
        self.pedidoDAO = PedidoDAO(conexion)
        self.lineaPedidoDAO = LineaPedidoDAO(conexion)

    def crearPedido(self, usuario_id, lista_tapas):
        pedido = PedidoVO(usuario_id)
        pedido_id = self.pedidoDAO.insertarPedido(pedido)

        for tapa_id, cantidad in lista_tapas:
            linea = LineaPedidoVO(pedido_id, tapa_id, cantidad)
            self.lineaPedidoDAO.insertarLineaPedido(linea)

        return pedido_id



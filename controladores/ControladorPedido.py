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
            # Validar stock antes de insertar
            cursor = self.pedidoDAO.db.cursor(dictionary=True)
            cursor.execute("SELECT stock FROM tapa WHERE id = %s", (tapa_id,))
            tapa = cursor.fetchone()

            if not tapa or tapa["stock"] < cantidad:
                raise Exception(f"No hay suficiente stock para la tapa con ID {tapa_id}")

            # Restar del stock
            nuevo_stock = tapa["stock"] - cantidad
            cursor.execute("UPDATE tapa SET stock = %s WHERE id = %s", (nuevo_stock, tapa_id))

            # Insertar línea de pedido
            linea = LineaPedidoVO(pedido_id, tapa_id, cantidad)
            self.lineaPedidoDAO.insertarLineaPedido(linea)

        self.pedidoDAO.db.commit()
        return pedido_id




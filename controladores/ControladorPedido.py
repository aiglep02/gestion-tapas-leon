from modelos.dao.pedidoDAO import PedidoDAO
from modelos.dao.LineaPedidoDAO import LineaPedidoDAO
from modelos.vo.pedidoVO import PedidoVO
from modelos.vo.LineaPedidoVO import LineaPedidoVO

class ControladorPedido:
    def __init__(self, conexion):
        self.pedidoDAO = PedidoDAO(conexion)
        self.lineaPedidoDAO = LineaPedidoDAO(conexion)
    """
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
    """
    def crearPedido(self, usuario_id, lista_tapas):
        pedido = PedidoVO(usuario_id)

        pedido.total = 0  # Inicializa el total a 0
        for tapa_id, cantidad in lista_tapas:
            # Obtén el precio de la tapa
            cursor = self.pedidoDAO.db.cursor(dictionary=True)
            cursor.execute("SELECT precio FROM tapa WHERE id = %s", (tapa_id,))
            tapa = cursor.fetchone()

            if tapa:
                precio_tapa = tapa['precio']
                pedido.total += precio_tapa * cantidad  # Sumar el total de la tapa con su cantidad

            # Crear la línea de pedido con solo el ID de la tapa (no pasas el precio aquí)
            linea = LineaPedidoVO(pedido.id, tapa_id, cantidad)
            self.lineaPedidoDAO.insertarLineaPedido(linea)

        # Inserta el pedido y actualiza el total después de calcularlo
        pedido_id = self.pedidoDAO.insertar_pedido(pedido)
        self.pedidoDAO.actualizar_total_pedido(pedido_id, pedido.total)
        self.pedidoDAO.db.commit()

        return pedido

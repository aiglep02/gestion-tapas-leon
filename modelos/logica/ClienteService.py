from modelos.dao.tapaDAO import TapaDAO
from modelos.dao.pedidoDAO import PedidoDAO
from modelos.vo.pedidoVO import PedidoVO

class ClienteService:
    def __init__(self, conexion):
        self.tapa_dao = TapaDAO(conexion)
        self.pedido_dao = PedidoDAO(conexion)

    def obtener_tapas_disponibles(self):
        """
        Devuelve lista de tapas con su stock actual.
        """
        return self.tapa_dao.obtener_todas_las_tapas()

    def hacer_pedido(self, id_usuario, id_tapa, cantidad):
        """
        Realiza un pedido si la tapa tiene stock disponible.
        Devuelve un mensaje de éxito o error.
        """
        tapas = self.tapa_dao.obtener_todas_las_tapas()
        tapa = next((t for t in tapas if t.id_tapa == id_tapa), None)

        if tapa is None:
            return False, "Tapa no válida."

        if tapa.stock == 0:
            return False, "Esta tapa no está disponible."

        if cantidad > tapa.stock:
            return False, f"Solo hay {tapa.stock} unidades disponibles."

        pedido = PedidoVO(id_usuario=id_usuario, id_tapa=id_tapa, cantidad=cantidad, estado="En preparación")
        id_pedido = self.pedido_dao.insertar_pedido(pedido)

        if id_pedido is None:
            return False, "Error al enviar el pedido."

        return True, "Tu pedido ha sido enviado a la cocina."

# modelos/logica/ClienteService.py

from modelos.dao.tapaDAO import TapaDAO
from modelos.dao.pedidoDAO import PedidoDAO
from modelos.vo.pedidoVO import PedidoVO

class ClienteService:
    def __init__(self):
        self.tapa_dao = TapaDAO()
        self.pedido_dao = PedidoDAO()

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
        tapa = next((t for t in tapas if t[0] == id_tapa), None)

        if tapa is None:
            return False, "Tapa no válida."

        if tapa[2] == 0:
            return False, "Esta tapa no está disponible."

        pedido = PedidoVO(id_usuario, id_tapa, cantidad, estado="En preparación")
        self.pedido_dao.insertar_pedido(pedido)

        return True, "Tu pedido ha sido enviado a la cocina."

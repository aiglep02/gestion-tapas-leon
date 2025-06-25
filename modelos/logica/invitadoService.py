from modelos.dao.tapaDAO import TapaDAO
from modelos.dao.pedidoDAO import PedidoDAO
from modelos.vo.pedidoVO import PedidoVO

class InvitadoService:
    def __init__(self):
        self.tapa_dao = TapaDAO()  
        self.pedido_dao = PedidoDAO()

    def obtener_tapas_disponibles(self):
        """
        Devuelve la lista de tapas con su stock actual, usando VO.
        """
        return self.tapa_dao.obtener_todas_las_tapas()

    def hacer_pedido_invitado(self, id_tapa, cantidad):
        """
        Realiza un pedido sin usuario registrado (invitado).
        Se asigna un id_usuario fijo para invitado.
        Devuelve (exito: bool, mensaje: str)
        """
        tapas = self.tapa_dao.obtener_todas_las_tapas()
        tapa = next((t for t in tapas if t.id_tapa == id_tapa), None)

        if tapa is None:
            return False, "Tapa no válida."

        if tapa.stock == 0:
            return False, "Esta tapa no está disponible."

        # Usamos id_usuario fijo para invitado, por ejemplo 38
        pedido = PedidoVO(id_usuario=38, id_tapa=id_tapa, cantidad=cantidad, estado="En preparación")
        id_pedido = self.pedido_dao.insertar_pedido(pedido)

        if id_pedido is None:
            return False, "No se pudo registrar el pedido."

        return True, "Tu pedido ha sido enviado a la cocina."

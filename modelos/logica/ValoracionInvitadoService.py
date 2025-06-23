from modelos.dao.valoracionDAO import ValoracionDAO
from modelos.dao.pedidoDAO import PedidoDAO
from modelos.vo.valoracionVO import ValoracionVO
from modelos.vo.tapaVO import TapaVO

class ValoracionService:
    def __init__(self, conexion):
        self.valoracion_dao = ValoracionDAO(conexion)
        self.pedido_dao = PedidoDAO(conexion)

    def obtener_tapas_entregadas(self, usuario_id):
        pedidos = self.pedido_dao.obtener_pedidos_entregados_por_usuario(usuario_id)
        # Convertimos a TapaVO solo con id y nombre
        tapas = [TapaVO(id_tapa=id_tapa, nombre=nombre) for id_tapa, nombre in pedidos]
        return tapas

    def insertar_valoracion(self, usuario_id, id_tapa, puntuacion, comentario):
        valoracion = ValoracionVO(
            id_usuario=usuario_id,
            id_tapa=id_tapa,
            puntuacion=puntuacion,
            comentario=comentario
        )
        return self.valoracion_dao.insertar_valoracion(valoracion)
